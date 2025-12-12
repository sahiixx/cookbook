module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'quickstarts/file-api/**/*.js',
    '!**/node_modules/**',
    '!**/coverage/**'
  ],
  testMatch: [
    '**/tests/unit/**/*.test.js',
    '**/tests/unit/**/*.spec.js'
  ],
  verbose: true,
  testTimeout: 10000
};