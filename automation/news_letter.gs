
function myFunction() {
  data = fetchDataFromExcel();

  for (var i = 0; i < data.length; i++) {
    for (var j = 0; j < data[i].length; j++) {
      Logger.log('Row ' + (i + 1) + ', Column ' + (j + 1) + ': ' + data[i][j]);

      var subject = "Subscribed News Letter";
      jsonContent = fetchAndParseJSON();

      GmailApp.sendEmail(data[i][j], subject, '', {
        htmlBody: jsonContent
      });
    }
  }
}

function fetchAndParseJSON() {
  var url = "https://imvickykumar999.pythonanywhere.com/";
  var response = UrlFetchApp.fetch(url);
  var jsonContent = response.getContentText();
  return jsonContent;
}

function fetchDataFromExcel() {
  var spreadsheetId = '1akZpxtRhFIm97X9ZIdlAm10nfs0_drWTo40rVvkI6zs';
  var sheetName = 'Sheet1';

  var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  var sheet = spreadsheet.getSheetByName(sheetName);
  var data = sheet.getDataRange().getValues();

  Logger.log(data);
  return data;
}


// Execution log

// 11:29:47 AM	Notice	Execution started
// 11:29:47 AM	Info	[[18erecs080.vicky@rietjaipur.ac.in], [sagar.sws2000@gmail.com], [hellovickykumar123@gmail.com]]
// 11:29:47 AM	Info	Row 1, Column 1: 18erecs080.vicky@rietjaipur.ac.in
// 11:29:48 AM	Info	Row 2, Column 1: sagar.sws2000@gmail.com
// 11:29:48 AM	Info	Row 3, Column 1: hellovickykumar123@gmail.com
// 11:29:49 AM	Notice	Execution completed
