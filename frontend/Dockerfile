# Use Node.js LTS
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Expose Next.js port
EXPOSE 3000

# Start Next.js
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]