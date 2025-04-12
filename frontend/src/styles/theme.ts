export const theme = {
  colors: {
    primary: 'hsl(var(--primary))',
    secondary: 'hsl(262.1 83.3% 57.8%)',
    background: 'hsl(var(--background))',
    foreground: 'hsl(var(--foreground))',
    border: 'hsl(var(--border))',
    muted: 'hsl(var(--muted))',
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem'
  },
  radii: {
    sm: '4px',
    md: '8px',
    lg: '12px'
  }
} as const;

export type Theme = typeof theme;