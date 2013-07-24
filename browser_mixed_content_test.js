/*

ad-hoc mochitests for bug 822367

NOTE: This test requires downloading a CSV file of top domains from Alexa's web site
Also note: This test is quite a hack.

*/



const PREF_DISPLAY = "security.mixed_content.block_display_content";
const PREF_ACTIVE = "security.mixed_content.block_active_content";
const gHttpTestRoot = "http://example.com/browser/browser/base/content/test/";
var origBlockDisplay;
var origBlockActive;
var gTestBrowser = null;
var urlIndex = 0;
var interval;
var rawDomList;
var domList;
var testURL = "https://people.mozilla.com/~tvyas/mixedcontent.html";
var numURLs = 8667;

function reqListener () 
{
	rawDomList = this.responseText.split("\n");

	var temp = new Array();

	// only use first 1000 domains - just for testing purposes

	for (var i=0;i<numURLs;i++)
	{
		temp.push ( "https://" + rawDomList[i].split(",")[1] );
		temp.push ( "https://www." + rawDomList[i].split(",")[1] );
	}
	domList = temp;

	firstTest(domList[urlIndex]);
}
 
function loadDomains ()
{
  var oReq = new XMLHttpRequest();
  oReq.onload = reqListener;
  oReq.open("get", gHttpTestRoot + "top-1m.csv", true); // substitute your own URL/CSV here
  oReq.send();
}

function urlNumber()
{
	return Math.floor ( urlIndex/2 );
}

registerCleanupFunction(function() {
  // Set preferences back to their original values
  Services.prefs.setBoolPref(PREF_DISPLAY, origBlockDisplay);
  Services.prefs.setBoolPref(PREF_ACTIVE, origBlockActive);
});

function MixedTestsCompleted() {
  //gTestBrowser.removeEventListener("load", checkForMixedContent, true);
  //gTestBrowser.removeEventListener("error", handleError, true);

  gBrowser.removeCurrentTab();
  window.focus();
  finish();
}

function test() {
  requestLongerTimeout(5000);
  waitForExplicitFinish();

  origBlockDisplay = Services.prefs.getBoolPref(PREF_DISPLAY);
  origBlockActive = Services.prefs.getBoolPref(PREF_ACTIVE);

  Services.prefs.setBoolPref(PREF_DISPLAY, false);  //Note mixed display is currently not going to be blocked by default
  Services.prefs.setBoolPref(PREF_ACTIVE, true);

  var newTab = gBrowser.addTab();
  gBrowser.selectedTab = newTab;
  gTestBrowser = gBrowser.selectedBrowser;
  newTab.linkedBrowser.stop()
  loadDomains();
}

function loadBlankPage()
{
  gTestBrowser.contentWindow.location = "about:blank";
}

function firstTest(url)
{
  //gTestBrowser.addEventListener("load", checkForMixedContent, true);
  //gTestBrowser.addEventListener("error", handleError, true);
  gTestBrowser.contentWindow.location = url;
  interval = setInterval ( cleanup, 10000 );
}


function handleError () {
  ok ( false, "Error loading site - error event: (" + urlNumber() + ")" + domList[urlIndex] );
  nextURL();
}

function cleanup () {
  clearInterval ( interval );
  var notification = PopupNotifications.getNotification("mixed-content-blocked", gTestBrowser);
  if ( notification ) {
    ok( false, "Mixed Content Doorhanger appeared: (" + urlNumber() + ")" + domList[urlIndex]);
  }


  // An aborted attempt at sussing out error conditions

  //var pageTitle = gTestBrowser.contentWindow.document.title;
  //if ( pageTitle === "Untrusted Connection" ) {
    //ok ( false, "Error loading site - Untrusted Connection: (" + urlNumber() + ")" + domList[urlIndex] );
  // } else if ( notification ) {
  //   ok( false, "Mixed Content Doorhanger appeared: (" + urlNumber() + ")" + domList[urlIndex]);
  // } else {
    //ok ( false, "Error loading site - timeout: (" + urlNumber() + ")" + domList[urlIndex] );
  //}

  loadBlankPage(); // get rid of any lingering doorhanger, false positive... also doesn't work
  nextURL();
}

function checkForMixedContent() {
  if ( interval ) clearInterval ( interval );
  var notification = PopupNotifications.getNotification("mixed-content-blocked", gTestBrowser);
  ok(!notification, "Mixed Content Doorhanger appeared: (" + urlNumber() + ")" + domList[urlIndex]);
  nextURL();
}

function nextURL() {
  //if ( interval ) clearInterval ( interval );
  urlIndex++;
  if ( urlIndex >= (2*numURLs) ) // rawDomList.length will happen later
  {
    MixedTestsCompleted();
  } else {
    interval = setInterval ( cleanup, 15000 );
    gTestBrowser.contentWindow.location = domList[urlIndex];
  }
}


