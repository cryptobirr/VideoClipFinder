# Frontend Dockerfile (React + Vite + TypeScript)
FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

# Expose port
EXPOSE 5173

# Run dev server
CMD ["pnpm", "dev", "--host"]
