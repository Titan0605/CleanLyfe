/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./app/static/**/*.{html,js,css}"],
    theme: {
        extend: {
            colors: {
                cleanlyfe: {
                    verdesote: '#06b865',
                    blue: '#09a5b9',
                },
            },
        },
    },
    plugins: [],
};