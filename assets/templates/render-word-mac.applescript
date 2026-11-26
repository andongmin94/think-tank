-- Microsoft Word for Mac counterpart of render-word.ps1.
-- Usage: osascript render-word-mac.applescript render|metrics SOURCE.docx TARGET.pdf|"" \
--          REFERENCE_HEADING_STYLE REFERENCE_ENTRY_STYLE ABSTRACT_LABEL TEMPLATE_FONTS
-- Opens the exact staged DOCX read-only, never saves it, and prints one JSON object.
-- Any statistic Word cannot provide is omitted; the Python caller then reports
-- native measurement as failed instead of substituting an estimate.
use AppleScript version "2.7"
use scripting additions
use framework "Foundation"
use framework "AppKit"

on run argv
	set mode to item 1 of argv
	set sourcePath to item 2 of argv
	set targetPath to item 3 of argv
	set referenceHeadingStyle to item 4 of argv
	set referenceEntryStyle to item 5 of argv
	set abstractLabel to item 6 of argv
	set templateFonts to item 7 of argv
	if application id "com.microsoft.Word" is running then error "Quit Microsoft Word first; native rendering must own an empty Word instance and never touches open documents." number 1001
	set hfsSource to (POSIX file sourcePath) as text
	set fields to {}
	set doc to missing value
	tell application id "com.microsoft.Word"
		launch
		try
			set display alerts to alerts none
		end try
		try
			open file name hfsSource read only true add to recent files false
			set doc to active document
			set end of fields to my pair("version", my jsonText(version as text))
			try
				repaginate doc
			end try
			set end of fields to my pair("pages", my statistic(doc, "pages"))
			try
				set end of fields to my pair("read_only", my jsonBool(read only of doc))
			end try
			if mode is "metrics" then
				set end of fields to my pair("whole_words", my statistic(doc, "words"))
				set contentEnd to end of content of text object of doc
				set bodyEnd to contentEnd
				set referenceFound to false
				set referenceCount to 0
				set abstractWords to 0
				repeat with currentParagraph in (paragraphs of doc)
					set paragraphRange to text object of currentParagraph
					set paragraphText to content of paragraphRange
					set styleName to name local of (style of currentParagraph)
					set trimmed to my trimText(paragraphText)
					if styleName is referenceHeadingStyle and trimmed is "References" and not referenceFound then
						set referenceFound to true
						if (start of content of paragraphRange) < bodyEnd then set bodyEnd to start of content of paragraphRange
					end if
					if styleName is "AuthorBioHead" then
						if (start of content of paragraphRange) < bodyEnd then set bodyEnd to start of content of paragraphRange
					end if
					if styleName is referenceEntryStyle and trimmed is not "" then set referenceCount to referenceCount + 1
					if styleName is "Abstract" then
						set abstractStart to start of content of paragraphRange
						if abstractLabel is not "" and paragraphText starts with abstractLabel then set abstractStart to abstractStart + (length of abstractLabel)
						set abstractRange to create range doc start abstractStart end (end of content of paragraphRange)
						set abstractWords to abstractWords + (my statistic(abstractRange, "words"))
					end if
				end repeat
				set end of fields to my pair("reference_heading_found", my jsonBool(referenceFound))
				set end of fields to my pair("reference_count", referenceCount)
				set end of fields to my pair("abstract_words", abstractWords)
				set end of fields to my pair("body_words", my statistic(create range doc start 0 end bodyEnd, "words"))
				set bodyTables to 0
				set bodyTableWords to 0
				repeat with currentTable in (tables of doc)
					set tableRange to text object of currentTable
					if (end of content of tableRange) ≤ bodyEnd then
						set bodyTables to bodyTables + 1
						set bodyTableWords to bodyTableWords + (my statistic(tableRange, "words"))
					end if
				end repeat
				set end of fields to my pair("body_tables", bodyTables)
				set end of fields to my pair("body_table_words", bodyTableWords)
				set end of fields to my pair("tables", count of tables of doc)
				set inlineCount to count of inline shapes of doc
				set floatingCount to count of shapes of doc
				set end of fields to my pair("figures", inlineCount + floatingCount)
				set bodyFigures to 0
				repeat with currentShape in (inline shapes of doc)
					set shapeRange to text object of currentShape
					if (story type of shapeRange) is main text story and (end of content of shapeRange) ≤ bodyEnd then set bodyFigures to bodyFigures + 1
				end repeat
				repeat with currentShape in (shapes of doc)
					set anchorRange to anchor of currentShape
					if (story type of anchorRange) is main text story and (end of content of anchorRange) ≤ bodyEnd then set bodyFigures to bodyFigures + 1
				end repeat
				set end of fields to my pair("body_figures", bodyFigures)
			else
				set hfsTarget to (POSIX file targetPath) as text
				save as doc file name hfsTarget file format format PDF
			end if
		on error errorText number errorNumber
			try
				if doc is not missing value then close doc saving no
			end try
			quit saving no
			error errorText number errorNumber
		end try
		try
			close doc saving no
		end try
		quit saving no
	end tell
	set end of fields to my pair("missing_template_fonts", my missingFonts(templateFonts))
	set end of fields to my pair("platform", my jsonText("macOS"))
	set AppleScript's text item delimiters to ","
	set body to fields as text
	set AppleScript's text item delimiters to ""
	return "{" & body & "}"
end run

on statistic(target, kind)
	tell application id "com.microsoft.Word"
		if kind is "words" then
			return compute statistics target statistic statistic words
		else
			return compute statistics target statistic statistic pages
		end if
	end tell
end statistic

on missingFonts(templateFonts)
	set installed to (current application's NSFontManager's sharedFontManager()'s availableFontFamilies()) as list
	set AppleScript's text item delimiters to ","
	set wanted to text items of templateFonts
	set AppleScript's text item delimiters to ""
	set missing to {}
	repeat with fontName in wanted
		set fontName to fontName as text
		if fontName is not "" and installed does not contain fontName then set end of missing to my jsonText(fontName)
	end repeat
	set AppleScript's text item delimiters to ","
	set joined to missing as text
	set AppleScript's text item delimiters to ""
	return "[" & joined & "]"
end missingFonts

on pair(key, value)
	return my jsonText(key) & ":" & (value as text)
end pair

on jsonBool(flag)
	if flag then return "true"
	return "false"
end jsonBool

on jsonText(value)
	set escaped to (current application's NSString's stringWithString:(value as text))
	set escaped to (escaped's stringByReplacingOccurrencesOfString:"\\" withString:"\\\\")
	set escaped to (escaped's stringByReplacingOccurrencesOfString:"\"" withString:"\\\"")
	set escaped to (escaped's stringByReplacingOccurrencesOfString:(character id 10) withString:"\\n")
	set escaped to (escaped's stringByReplacingOccurrencesOfString:(character id 13) withString:"\\r")
	set escaped to (escaped's stringByReplacingOccurrencesOfString:(character id 9) withString:"\\t")
	return "\"" & (escaped as text) & "\""
end jsonText

on trimText(value)
	set trimmed to (current application's NSString's stringWithString:(value as text))'s stringByTrimmingCharactersInSet:(current application's NSCharacterSet's whitespaceAndNewlineCharacterSet())
	return trimmed as text
end trimText
