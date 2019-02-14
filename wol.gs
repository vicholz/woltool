/*

WOL Tool
--------

GET  response with HOST, MAC, and WAKE data from cells.
POST accepts HOST, MAC, WAKE, and STATUS data then updates cells with WAKE/STATUS.

*/

function doPost(e){
  if (e.postData.contents){
    var data = JSON.parse(e.postData.contents)
    var range = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('WOL').getRange("A2:C20");
    var numRows = range.getNumRows();
    for (var i = 1; i <= numRows; i++) {
      var cell = range.getCell(i,1);
      if (!cell.isBlank()){
        var host = cell.getValue();
        if (data[host]){
          if (data[host]["wake"]) cell.offset(0,2).setValue(data[host]["wake"]);
          if (data[host]["status"]) cell.offset(0,3).setValue(data[host]["status"]);
        }
      }
    }
    return ContentService.createTextOutput("OK");
  }
  return ContentService.createTextOutput("ERROR");
}

function doGet(e) {
  var data = {};
  var range = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('WOL').getRange("A2:C20");
  var numRows = range.getNumRows();
  for (var i = 1; i <= numRows; i++) {
    var cell = range.getCell(i,1);
    if (!cell.isBlank()){
      var host  = cell.getValue();
      var mac   = cell.offset(0,1).getValue();
      var wake   = cell.offset(0,2).getValue(); 
      data[host] = {
        'mac': mac,
        'wake': wake,
      }
    }
  }
  return ContentService.createTextOutput(JSON.stringify(data,null,4)).setMimeType(ContentService.MimeType.JSON);
}