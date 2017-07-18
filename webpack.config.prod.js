var webpack = require('webpack');

module.exports = {
    plugins: [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({minimize: true})
    ]
};