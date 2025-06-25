// frontend/prettier.config.js

/** @type {import("prettier").Config} */
module.exports = {
  semi: true,                // Add semicolons at the end of statements
  singleQuote: true,         // Use single quotes instead of double
  trailingComma: 'es5',      // Add trailing commas where valid in ES5 (objects, arrays, etc.)
  printWidth: 80,            // Wrap lines at 80 characters
  tabWidth: 2,               // Number of spaces per tab
  useTabs: false,            // Indent with spaces, not tabs
  bracketSpacing: true,      // Print spaces between brackets in object literals
  arrowParens: 'always',     // Always include parens for arrow functions
  endOfLine: 'auto',         // Maintain existing line endings (useful for cross-platform)
};
