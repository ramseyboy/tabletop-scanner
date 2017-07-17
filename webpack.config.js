var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var merge = require('extendify')({ isDeep: true, arrays: 'concat' });
var devConfig = require('./webpack.config.dev');
var prodConfig = require('./webpack.config.prod');
var isDevelopment = true;
var extractCSS = new ExtractTextPlugin('exchange.css');

module.exports = merge({
    resolve: {
        extensions: [ '', '.js', '.jsx' ]
    },
    module: {
        loaders: [
            {
                loader: "babel-loader",

                // Skip any files outside of your project's `src` directory
                include: [
                    path.resolve(__dirname, "tabletopscanner-client"),
                ],

                // Only run `.js` and `.jsx` files through Babel
                test: /\.jsx?$/,

                // Options to configure babel with
                query: {
                    plugins: ['transform-runtime'],
                    presets: ['es2015', 'stage-0', 'react'],
                }
            },
            { test: /\.css/, loader: extractCSS.extract(['css-loader']) },
            {
                test: /\.png$/,
                loader: 'url-loader',
                query: { mimetype: 'image/png' }
            }
        ]
    },
    entry: [
        // Set up an ES6-ish environment
        'babel-polyfill',

        // Add your application's scripts below
        './tabletopscanner-client/index.jsx'
    ],
    output: {
        path: path.join(__dirname, 'tabletopscanner/static', 'dist'),
        filename: 'bundle.js',
        publicPath: '/dist/'
    },
    plugins: [
        extractCSS
    ]
}, isDevelopment ? devConfig : prodConfig);