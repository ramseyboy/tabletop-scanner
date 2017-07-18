var path = require('path');
var webpack = require('webpack');
var merge = require('extendify')({isDeep: true, arrays: 'concat'});
var devConfig = require('./webpack.config.dev');
var prodConfig = require('./webpack.config.prod');

var build = require('./webpack.consts');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = (env) => {
    var isDebug = !env.prod;
    return merge({
        entry: [
            // Set up an ES6-ish environment
            'babel-polyfill',

            // Add your application's scripts below
            './tabletopscanner-client/index.jsx'
        ],
        output: {
            path: path.join(__dirname, build.OUTPUT_DIR, 'dist'),
            filename: build.OUTPUT_ARTIFACT + ".js",
            publicPath: '/dist/'
        },
        resolve: {
            extensions: ['.js', '.jsx', '.css']
        },
        module: {
            rules: [
                {
                    // Only run `.js` and `.jsx` files through Babel
                    test: /\.jsx?$/,

                    use: {
                        loader: "babel-loader",
                        // Options to configure babel with
                        query: {
                            plugins: ['transform-runtime'],
                            presets: ['es2015', 'stage-0', 'react']
                        }
                    },

                    // Skip any files outside of your project's `src` directory
                    include: [
                        path.resolve(__dirname, build.CLIENT_DIR)
                    ]
                },
                {
                    test: /\.png$/,
                    use: {
                        loader: 'url-loader',
                        query: {
                            mimetype: 'image/png'
                        }
                    }
                },
                {
                    test: /\.css$/,
                    loader: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: 'css-loader?modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]!postcss-loader'
                    })
                }

            ]
        },
        plugins: [
            new ExtractTextPlugin({
                filename: "styles.css",
                allChunks: true
            })
        ]
    }, isDebug ? devConfig : prodConfig)
};