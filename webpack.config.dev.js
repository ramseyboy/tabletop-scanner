var path = require('path');
var webpack = require('webpack');

var build = require('./webpack.consts');

module.exports = {
    plugins: [
        // Plugins that apply in development builds only
        new webpack.SourceMapDevToolPlugin({
            filename: '[file].map', // Remove this line if you prefer inline source maps
            moduleFilenameTemplate: path.relative(build.OUTPUT_DIR + '/dist', '[resourcePath]') // Point sourcemap entries to the original file locations on disk
        })
    ]
};