const nextJest = require('next/jest');

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
});

// Add any custom config to be passed to Jest
/** @type {import('jest').Config} */
const customJestConfig = {
  moduleDirectories: ['node_modules', '<rootDir>/'],
  moduleNameMapper: {
    '^@/(.*)$': [
      '<rootDir>/components/$1',
      '<rootDir>/pages/$1',
      '<rootDir>/__test__/$1',
    ],
  },
  testEnvironmentOptions: {
    customExportConditions: [''],
  },
  testEnvironment: 'jest-environment-jsdom',
  testTimeout: 20000,
};

module.exports = createJestConfig(customJestConfig);
