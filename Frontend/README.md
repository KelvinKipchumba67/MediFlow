# MediFlow Frontend - Quick Start Guide

Welcome to the frontend repo! We are building the Context-Aware Triage System interface. To keep things incredibly fast and lightweight for the hackathon, we are using Vite + React with Pure Custom CSS (no heavy UI libraries).

## 1. Local Setup

Before running the frontend, ensure the Python AI backend (main.py) is already running on port 8000 (otherwise, the UI will throw a network error when trying to fetch the ML predictions).

Navigate to the frontend directory:

Bash(any cli)
cd frontend
Install dependencies:

Bash(any cli)
npm install
Start the Vite development server:

Bash (any cli)
npm run dev
Open your browser to http://localhost:5173.

## 2. Architecture Overview

Framework: React via Vite (gives us instant hot-reloading).

Styling (src/index.css): We are using CSS Variables for a custom "High-Tech Dark Mode" aesthetic. To change the theme globally, just update the variables at the top of the file (e.g., --primary, --danger).

State Management: Standard React useState. The form maintains a formData object that perfectly matches the PatientData Pydantic model on the backend.

API Communication: The form uses the native fetch API to send a POST request to http://localhost:8000/triage.
Note: The backend handles translating our HTML Checkboxes (true/false) into API Integers (1/0).

## 3. Key Files to Know

src/App.jsx - The main wrapper and layout container.

src/components/PatientIntakeForm.jsx - The core engine of the UI. It handles state, form submission, and displaying the AI's Intelligence Report.

src/index.css - Contains our CSS Grid layouts (.input-grid-2, .input-grid-3), custom glowing toggle switches, and responsive inputs.
