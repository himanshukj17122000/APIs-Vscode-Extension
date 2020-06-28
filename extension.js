const vscode = require('vscode');
const axios = require('axios').default;
const fs = require('fs');
const path = require('path');
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Congratulations, your extension "apimate" is now active!');

  async function APICall(value) {
    var searchStrings = value.split(',');
    value = searchStrings[0].trim();
    var fileName = searchStrings[1] ?
      searchStrings[1].trim() + '.json' :
      'APIlist.json';
    var data = {};
    const folderPath = vscode.workspace.workspaceFolders[0].uri
      .toString()
      .split(':')[1];
    await axios
      .get(`https://flask-apillist.herokuapp.com/${value}`)
      .then(response => {
        data = response;
        return;
      })
      .catch(error => {
        var myError = [" Please Try Again "]
        fs.writeFile(
          path.join(folderPath, fileName),
          JSON.stringify(myError),
          err => {
            if (err) {
              console.log(err);
              vscode.window.showErrorMessage('Failed to create ' + fileName);
            }
            vscode.window.showInformationMessage('Created ' + fileName);
          }
        );
      });

    fs.writeFile(
      path.join(folderPath, fileName),
      JSON.stringify(data.data),
      err => {
        if (err) {
          console.log(err);
          vscode.window.showErrorMessage('Failed to create ' + fileName);
        }
        vscode.window.showInformationMessage('Created ' + fileName);
      }
    );
  }

  let disposable = vscode.commands.registerCommand(
    'apimate.getList',
    function () {
      vscode.window.showInputBox().then(value => {
        APICall(value);
        // setInterval(function () {
        //   APICall(value);
        // }, 10000000);
      });
    }
  );

  context.subscriptions.push(disposable);
}
exports.activate = activate;

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};