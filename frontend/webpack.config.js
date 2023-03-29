const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const {VueLoaderPlugin} = require("vue-loader");
const {CleanWebpackPlugin} = require("clean-webpack-plugin");
const TerserPlugin = require('terser-webpack-plugin');


const src = path.resolve(__dirname, 'src');
const dist = path.resolve(__dirname, '../streamfield/static/streamfield/');


module.exports = (env, argv) => {
  const IS_PRODUCTION = argv.mode === 'production';

  const config = {
    entry: {
      streamfield_widget: './src/streamfield_widget.js', 
      admin_popup_response: './src/admin_popup_response.js'
    },
    output: {
      path: dist,
      filename: "[name].js",
    },

    resolve: {
      alias: {
        "@": src
      }
    },
    mode: argv.mode,
    devServer: {
      static: dist,
      // to be able to visit dev server from phones and other computers in your network
      allowedHosts: 'all'
    },
    plugins: [
      new VueLoaderPlugin(),
      new CleanWebpackPlugin(),
    ],
    module: {
      rules: [{
        test: /\.vue$/,
        loader: "vue-loader",
        exclude: /node_modules/
      },
      {
        test: /\.sass$/,
        exclude: /node_modules/,
        use: [
          IS_PRODUCTION ? MiniCssExtractPlugin.loader : "style-loader",
          {
            loader: "css-loader"
          },
          {
            loader: 'sass-loader',
            options: {
              sassOptions: {
                indentedSyntax: true
              }
            }
          }
        ]
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/
      }]
    },
    optimization: {
      minimizer: [
        // extend default plugins
        // `...`,
        new TerserPlugin({
          extractComments: false,
          terserOptions: {
            format: {
              comments: false,
            },
          },
        }),
        // HTML and JS are minified by default if config.mode === production.
        // But for CSS we need to add this:
        new CssMinimizerPlugin()
      ]
    }
  };


  if (IS_PRODUCTION) {
    // put all CSS files to a single <link rel="stylesheet" href="...">
    config.plugins.push(new MiniCssExtractPlugin({
      filename: "streamfield_widget.css"
    }));

  }

  return config;
}