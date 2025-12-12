FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Expose port for Vite dev server
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
