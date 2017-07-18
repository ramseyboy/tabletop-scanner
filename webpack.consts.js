
module.exports = {
    CLIENT_DIR: "tabletopscanner-client",
    OUTPUT_DIR: "tabletopscanner/static",
    OUTPUT_ARTIFACT: "bundle",
    isDevelopment: function(env) {
        return env.debug === 'true';
    }
};
