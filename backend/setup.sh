#!/bin/bash

# AttachLink Django Backend Setup Script
# Automates the entire Django backend setup process

set -e  # Exit on error

echo "========================================="
echo "AttachLink Django Backend Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python version
echo -e "${YELLOW}Step 1: Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Step 2: Create virtual environment
echo -e "${YELLOW}Step 2: Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 4: Upgrade pip
echo -e "${YELLOW}Step 4: Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Step 5: Install dependencies
echo -e "${YELLOW}Step 5: Installing dependencies (this may take a few minutes)...${NC}"
pip install -r requirements.txt > /dev/null
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 6: Check .env file
echo -e "${YELLOW}Step 6: Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created from template${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Edit .env with your Supabase credentials${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Step 7: Run migrations
echo -e "${YELLOW}Step 7: Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migrations completed${NC}"
echo ""

# Step 8: Create superuser prompt
echo -e "${YELLOW}Step 8: Creating superuser...${NC}"
echo "Do you want to create a superuser now? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superuser created${NC}"
else
    echo "Skipping superuser creation. You can create one later with:"
    echo "python manage.py createsuperuser"
fi
echo ""

# Step 9: Collect static files
echo -e "${YELLOW}Step 9: Collecting static files...${NC}"
python manage.py collectstatic --noinput > /dev/null
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

# Summary
echo "========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your Supabase credentials"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000/api/v1/docs/"
echo ""
echo "Useful commands:"
echo "- Start dev server: python manage.py runserver"
echo "- Access Django admin: http://localhost:8000/admin/"
echo "- Run tests: pytest"
echo ""
