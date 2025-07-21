import os
import json
import uuid
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from .tools import ToolServices
from .code_gen import make_ai_request

class ExponentAgent:
    """All-purpose ML engineering assistant with context awareness and simple memory."""
    
    def __init__(self):
        self.tools = ToolServices()
        self.chat_history = []
        self.memory_store = {}  # Simple in-memory storage
        
        # Define available tools for function calling
        self.available_tools = [
            {
                "name": "create_project",
                "description": "Create a new ML project with folder structure and essential files",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "Name for the new project (auto-generated if not provided)"
                        },
                        "description": {
                            "type": "string", 
                            "description": "Description of the project"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "process_dataset",
                "description": "Analyze and process a dataset to understand its structure and content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dataset_path": {
                            "type": "string",
                            "description": "Path to the dataset file (will auto-detect if not provided)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "generate_training_code",
                "description": "Generate focused, dataset-specific training code with visualization and logging",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the ML task to implement"
                        },
                        "dataset_path": {
                            "type": "string",
                            "description": "Path to the dataset (will auto-detect if not provided)"
                        }
                    },
                    "required": ["task_description"]
                }
            },
            {
                "name": "run_training_job",
                "description": "Execute a training job using the generated code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID to run training for"
                        },
                        "dataset_path": {
                            "type": "string",
                            "description": "Path to the dataset"
                        },
                        "task_description": {
                            "type": "string",
                            "description": "Description of the training task"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "list_projects",
                "description": "List all available ML projects",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "debug_datasets",
                "description": "Debug dataset detection to see what files are found and where",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
        
    def store_in_memory(self, text: str, metadata: Dict[str, Any] = None):
        """Store text in simple memory."""
        id = f"{uuid.uuid4()}"
        self.memory_store[id] = {
            "text": text,
            "metadata": metadata or {}
        }
        return id
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant context from memory (simple keyword matching)."""
        results = []
        query_lower = query.lower()
        
        for item in self.memory_store.values():
            text = item["text"].lower()
            if any(word in text for word in query_lower.split()):
                results.append(item["text"])
                if len(results) >= top_k:
                    break
        
        return results
    
    def add_to_chat_history(self, role: str, content: str):
        """Add message to chat history and store in memory."""
        message = {"role": role, "content": content}
        self.chat_history.append(message)
        
        # Store in simple memory
        metadata = {
            "type": "chat",
            "role": role,
            "timestamp": str(uuid.uuid4()),  # Simple timestamp
            "text": content
        }
        self.store_in_memory(content, metadata)
    
    def index_codebase(self, path: str = "."):
        """Index codebase files in simple memory."""
        path_obj = Path(path)
        
        for file_path in path_obj.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata = {
                    "type": "code",
                    "file_path": str(file_path),
                    "language": "python",
                    "text": content
                }
                self.store_in_memory(content, metadata)
                
            except Exception as e:
                print(f"Error indexing {file_path}: {e}")
    
    def get_context_for_query(self, query: str) -> str:
        """Get relevant context for a query."""
        context_results = self.retrieve_context(query, top_k=3)
        
        if context_results:
            context = "\n\n".join(context_results)
            return f"Relevant context:\n{context}\n\nQuery: {query}"
        else:
            return query
    
    def _extract_function_calls(self, response: str) -> List[Dict[str, Any]]:
        """Extract function calls from LLM response using regex patterns."""
        function_calls = []
        
        # Pattern to match function calls like: <function>create_project</function>
        function_pattern = r'<function>(\w+)</function>'
        function_matches = re.findall(function_pattern, response)
        
        # Pattern to match parameters like: <param>name:value</param>
        param_pattern = r'<param>(\w+):([^<]+)</param>'
        
        for function_name in function_matches:
            # Find all parameters for this function
            params = {}
            
            # Find all parameter matches in the entire response
            param_matches = re.findall(param_pattern, response)
            
            for param_name, param_value in param_matches:
                params[param_name] = param_value.strip()
            
            function_calls.append({
                "tool": function_name,
                "params": params
            })
        
        return function_calls
    
    def _execute_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> str:
        """Execute detected tool calls and format response."""
        if not tool_calls:
            return "No specific tools detected for this request."
        
        results = []
        for tool_call in tool_calls:
            try:
                tool_name = tool_call["tool"]
                params = tool_call["params"]
                
                # Handle auto_detect parameters with improved dataset detection
                if "dataset_path" in params and (params["dataset_path"] == "auto_detect" or not params["dataset_path"] or params["dataset_path"] == ""):
                    # Get the original question for context-aware dataset selection
                    original_question = ""
                    if hasattr(self, '_current_question'):
                        original_question = self._current_question
                    
                    detected_dataset = self._detect_datasets(original_question)
                    if detected_dataset:
                        params["dataset_path"] = detected_dataset
                        results.append(f"🔍 Auto-detected dataset: {detected_dataset}")
                    else:
                        results.append("❌ No CSV datasets found in search directories")
                        results.append("📁 Searched directories: current directory, ~/.exponent, and subdirectories")
                        # Don't proceed with the tool call if no dataset found
                        continue
                elif "dataset_path" not in params:
                    # If dataset_path is not provided at all, try to auto-detect
                    # Get the original question for context-aware dataset selection
                    original_question = ""
                    if hasattr(self, '_current_question'):
                        original_question = self._current_question
                    
                    detected_dataset = self._detect_datasets(original_question)
                    if detected_dataset:
                        params["dataset_path"] = detected_dataset
                        results.append(f"🔍 Auto-detected dataset: {detected_dataset}")
                    else:
                        results.append("❌ No CSV datasets found in search directories")
                        results.append("📁 Searched directories: current directory, ~/.exponent, and subdirectories")
                        # Don't proceed with the tool call if no dataset found
                        continue
                
                if "project_name" in params and (params["project_name"] == "auto_generate" or not params["project_name"]):
                    # Generate a meaningful project name
                    params["project_name"] = "ML_Project_" + str(uuid.uuid4())[:8]
                
                # Execute the tool using correct method names
                if tool_name == "process_dataset":
                    result = self.tools.process_dataset(**params)
                elif tool_name == "create_project":
                    result = self.tools.create_project(**params)
                elif tool_name == "generate_training_code":
                    result = self.tools.generate_training_code(**params)
                elif tool_name == "run_training_job":
                    result = self.tools.run_training_job(**params)
                elif tool_name == "list_projects":
                    result = self.tools.list_projects()
                elif tool_name == "debug_datasets":
                    debug_info = self.debug_dataset_detection()
                    result = {"success": True, "message": debug_info}
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                # Format the result
                if result.get("success"):
                    results.append(f"✅ {tool_name}: {result.get('message', 'Completed successfully')}")
                else:
                    results.append(f"❌ {tool_name}: {result.get('error', 'Failed')}")
                    
            except Exception as e:
                results.append(f"❌ {tool_call['tool']}: Error - {str(e)}")
        
        return "\n".join(results)
    
    def _detect_datasets(self, query: str = "") -> Optional[str]:
        """Enhanced dataset detection that searches multiple directories with intelligent selection."""
        import os
        from pathlib import Path
        
        # Define search directories
        search_dirs = [
            ".",  # Current directory
            str(Path.home() / ".exponent"),  # Exponent base directory
        ]
        
        # Also search in subdirectories of .exponent
        exponent_dir = Path.home() / ".exponent"
        if exponent_dir.exists():
            for subdir in exponent_dir.iterdir():
                if subdir.is_dir():
                    search_dirs.append(str(subdir))
        
        csv_files = []
        
        for search_dir in search_dirs:
            try:
                if os.path.exists(search_dir):
                    for file in os.listdir(search_dir):
                        if file.endswith('.csv'):
                            full_path = os.path.join(search_dir, file)
                            csv_files.append(full_path)
            except Exception as e:
                print(f"Error searching directory {search_dir}: {e}")
        
        if not csv_files:
            return None
        
        # If we have a query, try to find the most relevant dataset
        if query:
            query_lower = query.lower()
            
            # Look for datasets that match the query keywords
            relevant_files = []
            for file_path in csv_files:
                file_name = os.path.basename(file_path).lower()
                
                # Check for specific dataset types based on query
                if any(keyword in query_lower for keyword in ['twitter', 'sentiment', 'social']):
                    if any(keyword in file_name for keyword in ['twitter', 'sentiment', 'social']):
                        relevant_files.append(file_path)
                
                elif any(keyword in query_lower for keyword in ['netflix', 'churn', 'customer']):
                    if any(keyword in file_name for keyword in ['netflix', 'churn', 'customer']):
                        relevant_files.append(file_path)
                
                elif any(keyword in query_lower for keyword in ['plant', 'disease', 'agriculture']):
                    if any(keyword in file_name for keyword in ['plant', 'disease', 'agriculture']):
                        relevant_files.append(file_path)
            
            # Return the most relevant file if found
            if relevant_files:
                return relevant_files[0]
        
        # Fallback to the first CSV file found
        return csv_files[0]
    
    def debug_dataset_detection(self) -> str:
        """Debug method to show what datasets are found and where."""
        import os
        from pathlib import Path
        
        debug_info = []
        debug_info.append("🔍 Dataset Detection Debug Report")
        debug_info.append("=" * 50)
        
        # Define search directories
        search_dirs = [
            ".",  # Current directory
            str(Path.home() / ".exponent"),  # Exponent base directory
        ]
        
        # Also search in subdirectories of .exponent
        exponent_dir = Path.home() / ".exponent"
        if exponent_dir.exists():
            for subdir in exponent_dir.iterdir():
                if subdir.is_dir():
                    search_dirs.append(str(subdir))
        
        total_csv_files = []
        
        for search_dir in search_dirs:
            debug_info.append(f"\n📁 Searching: {search_dir}")
            try:
                if os.path.exists(search_dir):
                    files = os.listdir(search_dir)
                    csv_files_in_dir = [f for f in files if f.endswith('.csv')]
                    
                    if csv_files_in_dir:
                        debug_info.append(f"   ✅ Found {len(csv_files_in_dir)} CSV files:")
                        for csv_file in csv_files_in_dir:
                            full_path = os.path.join(search_dir, csv_file)
                            total_csv_files.append(full_path)
                            debug_info.append(f"      - {csv_file} (full path: {full_path})")
                    else:
                        debug_info.append(f"   ❌ No CSV files found")
                else:
                    debug_info.append(f"   ❌ Directory does not exist")
            except Exception as e:
                debug_info.append(f"   ❌ Error accessing directory: {e}")
        
        debug_info.append(f"\n📊 Summary:")
        debug_info.append(f"   Total CSV files found: {len(total_csv_files)}")
        if total_csv_files:
            debug_info.append(f"   First file (will be used): {total_csv_files[0]}")
        
        return "\n".join(debug_info)
    
    def ask(self, question: str) -> str:
        """Ask the agent a question with function calling capabilities."""
        # Store the current question for context-aware dataset selection
        self._current_question = question
        
        # Get relevant context from memory
        context = self.get_context_for_query(question)
        
        # Add to chat history
        self.add_to_chat_history("user", question)
        
        # Build system prompt with available tools
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}" 
            for tool in self.available_tools
        ])
        
        system_prompt = f"""You are Exponent, an AI-powered ML engineering assistant. You help users with machine learning projects, code analysis, and technical questions.

**Available Tools:**
{tools_description}

**Function Calling Instructions:**
When the user asks you to perform actions, use the available tools by calling them with this format:
<function>tool_name</function>
<param>parameter_name:parameter_value</param>

For example:
<function>create_project</function>
<param>project_name:My ML Project</param>
<param>description:Customer churn prediction model</param>

**IMPORTANT: Dataset Detection**
When users mention datasets, models, or data analysis, ALWAYS use the process_dataset tool first to analyze available data. The tool will auto-detect CSV files in the current directory.

**Context from previous conversations:**
{context}

**User's question:** {question}

**Instructions:**
1. If the user asks you to perform actions (create projects, analyze data, generate code, etc.), use the appropriate tools.
2. If the user mentions datasets, models, or data analysis, ALWAYS start by calling process_dataset to analyze available data.
3. If the user asks general questions about ML concepts, provide helpful explanations.
4. Always be proactive and helpful - if you can take action, do so.
5. After using tools, explain what was accomplished and suggest next steps.

**Response:**"""
        
        try:
            # Generate response using LLM with function calling
            response = make_ai_request(system_prompt)
            
            # Extract function calls from response
            function_calls = self._extract_function_calls(response)
            
            # Execute tools if detected
            tool_results = ""
            if function_calls:
                tool_results = self._execute_tool_calls(function_calls)
                
                # If tools were executed successfully, add explanation
                if tool_results and "✅" in tool_results:
                    explanation_prompt = f"""The user asked: {question}

I have executed the following actions:
{tool_results}

Please provide a brief, helpful explanation of what was accomplished and what the user can do next. Keep it concise and actionable.

Response:"""
                    
                    try:
                        explanation = make_ai_request(explanation_prompt)
                        final_response = f"{tool_results}\n\n{explanation}"
                    except Exception as e:
                        final_response = f"{tool_results}\n\n✅ Actions completed successfully! The requested operations have been performed."
                    
                    # Add response to chat history
                    self.add_to_chat_history("assistant", final_response)
                    return final_response
            
            # If no tools were called, return the original response
            self.add_to_chat_history("assistant", response)
            return response
            
        except Exception as e:
            # Fallback response if LLM fails
            fallback_response = f"I apologize, but I encountered an error while processing your request: {str(e)}. Please check your API configuration and try again."
            self.add_to_chat_history("assistant", fallback_response)
            return fallback_response
    
    # Direct tool call methods for explicit usage (fixed to use correct method names)
    def process_dataset_tool(self, dataset_path: str = "auto_detect") -> Dict[str, Any]:
        """Process dataset tool call."""
        return self.tools.process_dataset(dataset_path=dataset_path)
    
    def create_project_tool(self, project_name: str = "auto_generate", description: str = "") -> Dict[str, Any]:
        """Create project tool call."""
        return self.tools.create_project(project_name=project_name, description=description)
    
    def generate_training_code_tool(self, task: str, project_id: str = "auto_detect") -> Dict[str, Any]:
        """Generate training code tool call."""
        return self.tools.generate_training_code(task_description=task, dataset_path=project_id)
    
    def run_training_job_tool(self, project_id: str = "auto_detect", dataset_path: str = "auto_detect") -> Dict[str, Any]:
        """Run training job tool call."""
        return self.tools.run_training_job(project_id=project_id, dataset_path=dataset_path, task_description="Training job", model_code="auto_generate")
    
    def deploy_model_tool(self, model_path: str = "auto_detect", provider: str = "github") -> Dict[str, Any]:
        """Deploy model tool call."""
        return self.tools.deploy_model(project_path=model_path, project_name=provider)
    
    def list_projects_tool(self) -> Dict[str, Any]:
        """List projects tool call."""
        projects = self.tools.list_projects()
        return {"success": True, "projects": projects}
    
    def get_project_info_tool(self, project_id: str) -> Dict[str, Any]:
        """Get project info tool call."""
        return self.tools.get_project_info(project_id=project_id)
    
    def get_status(self) -> str:
        """Get agent status including memory info."""
        return f"""
🤖 Exponent Agent Status
========================
Memory: Simple in-memory storage
Chat History: {len(self.chat_history)} messages
Memory Items: {len(self.memory_store)} stored
Tool Integration: ✅ Active
Available Tools: Dataset processing, Project creation, Code generation, Training jobs, Deployment
        """
    
    def clear_memory(self):
        """Clear all memory."""
        self.memory_store.clear()
        self.chat_history = []
        return "Memory cleared successfully!"
    
    def search_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search memory for relevant content."""
        results = []
        query_lower = query.lower()
        
        for item_id, item in self.memory_store.items():
            text = item["text"].lower()
            if any(word in text for word in query_lower.split()):
                results.append({
                    "id": item_id,
                    "text": item["text"],
                    "metadata": item["metadata"]
                })
                if len(results) >= top_k:
                    break
        
        return results 
