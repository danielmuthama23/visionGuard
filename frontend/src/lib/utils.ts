// src/lib/utils.ts

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import axios from 'axios';

/**
 * Merges CSS classes with Tailwind CSS and class variance authority support
 * @param inputs Class values to merge
 * @returns Merged class string
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formats a date to localized string
 * @param date Date object or string
 * @param options Intl.DateTimeFormat options
 * @returns Formatted date string
 */
export function formatDate(
  date: Date | string,
  options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }
): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', options);
}

/**
 * Handles API errors and returns consistent error object
 * @param error Unknown error
 * @returns Standardized error object
 */
export function handleApiError(error: unknown): { message: string } {
  if (axios.isAxiosError(error)) {
    return {
      message: error.response?.data?.message || error.message,
    };
  }

  if (error instanceof Error) {
    return { message: error.message };
  }

  return { message: 'An unknown error occurred' };
}

/**
 * Safely access localStorage with SSR support
 * @param key Storage key
 * @returns Stored value or null
 */
export function getLocalStorage(key: string): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(key);
}

/**
 * Safely set localStorage with SSR support
 * @param key Storage key
 * @param value Value to store
 */
export function setLocalStorage(key: string, value: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(key, value);
}

/**
 * Format currency values
 * @param amount Currency amount
 * @param currency ISO currency code (default: USD)
 * @returns Formatted currency string
 */
export function formatCurrency(
  amount: number,
  currency: string = 'USD'
): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

/**
 * Generate unique ID
 * @returns Random 8-character ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 10);
}

/**
 * Delay execution
 * @param ms Milliseconds to sleep
 * @returns Promise that resolves after delay
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}