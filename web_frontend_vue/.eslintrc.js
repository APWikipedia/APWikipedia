module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true
    },
    extends: [
        'plugin:vue/vue3-essential', // 或者 'plugin:vue/vue3-recommended' 根据你的需要
        'eslint:recommended'
    ],
    parserOptions: {
        ecmaVersion: 12,
        parser: '@babel/eslint-parser',
        requireConfigFile: false,
        sourceType: 'module'
    },
    plugins: [
        'vue'
    ],
    rules: {
        // 自定义规则或者修改规则
    }
};
