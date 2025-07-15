# Installation

## From PyPI (Recommended)

```bash
pip install exponent-ml
```

## From Source

```bash
git clone https://github.com/yourusername/exponent-ml.git
cd exponent-ml
pip install -e .
```

## Authentication Setup

1. Create a Clerk account at [clerk.com](https://clerk.com)
2. Create a new application
3. Add your Clerk keys to environment:

```bash
export CLERK_PUBLISHABLE_KEY="pk_test_..."
export CLERK_SECRET_KEY="sk_test_..."
```

4. Run `exponent login` to authenticate 