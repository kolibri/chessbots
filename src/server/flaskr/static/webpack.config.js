/*** webpack.config.js ***/
const path = require('path');
module.exports = {
    mode: 'development',
    entry: path.join(__dirname, "app.js"),
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                use: "babel-loader",
                exclude: /node_modules/
            },
            {
                test: /\.*css$/,
                use : ['style-loader',
                        'css-loader',
                        'sass-loader'
                    ]
            },
        ]
    },
    resolve: {
        extensions: [".js", ".jsx", ".css", "scss"]
    }
};
