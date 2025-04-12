// import { defineConfig } from 'vite';
// import react from '@vitejs/plugin-react';
// import path from 'path';

// export default defineConfig({
//   plugins: [react()],
//   server: {
//     port: 5173,
//     strictPort: true,
//     open: true
//   },
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, 'src'),
//       '@components': path.resolve(__dirname, 'src/components'),
//       '@pages': path.resolve(__dirname, 'src/pages'),
//       '@public': path.resolve(__dirname, 'public')
//     }
//   },
//   build: {
//     outDir: 'dist',
//     emptyOutDir: true,
//     rollupOptions: {
//       input: {
//         main: path.resolve(__dirname, 'index.html')
//       }
//     }
//   }
// });

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, './'), // Explicit root path
  publicDir: resolve(__dirname, 'public'), // Explicit public directory
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html') // Explicit entry point
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  }
})