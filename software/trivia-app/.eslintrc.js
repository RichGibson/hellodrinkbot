module.exports = {
    parserOptions: {
      ecmaVersion: 2019,
      sourceType: 'module'
    },
    env: {
      es6: true,
      browser: true,
      node: true,
      "jest/globals": true
    },
    extends: [
      'eslint:recommended'
    ],
    plugins: [
      'svelte3',
      'jest'
    ],
    ignorePatterns: [
      'public/build/'
    ],
    overrides: [
      {
        files: ['**/*.svelte'],
        processor: 'svelte3/svelte3'
      }
    ],
    rules: {
      // semi: ['error', 'never'] // uncomment if you want to remove ;
      "jest/no-disabled-tests": "warn",
      "jest/no-focused-tests": "error",
      "jest/no-identical-title": "error",
      "jest/prefer-to-have-length": "warn",
      "jest/valid-expect": "error"
    },
    settings: {
      // ...
    }
  }