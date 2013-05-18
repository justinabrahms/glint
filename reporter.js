/*
{
  file:        [string, filename]
  error: {
    id:        [string, usually '(error)'],
    code:      [string, error/warning code],
    reason:    [string, error/warning message],
    evidence:  [string, a piece of code that generated this error]
    line:      [number]
    character: [number]
    scope:     [string, message scope;
                usually '(main)' unless the code was eval'ed]

    [+ a few other legacy fields that you don't need to worry about.]
  }
}

"glint.py:2:1: F401 'json' imported but unused"

This is a super simple reporter to make it more like pylints output
*/

"use strict";

module.exports = {
	reporter: function (res) {
		var len = res.length;
		var str = "";

		res.forEach(function (r) {
			var file = r.file;
			var err = r.error;

			str += file + ":" + err.line + ":" +
				err.character + ": " + err.code + " " + err.reason + "\n";
		});

		if (str) {
			process.stdout.write(str);
		}
	}
};