
generateBookHTML(bookID,bookName,bookAuthor,bookInfo,booklLink,bookIcon);
console.log(bookList);
function generateBookHTML(bookID,bookName,bookAuthor,bookInfo,bookLink,bookIcon)
{
    bookHTML+="<div id=\""+bookID+"\" class=\"templatemo_buy_product_box\">\n" +
        "            \t<h1>"+bookName+" <span>(by "+bookAuthor+")</span></h1>\n" +
        "   \t            <img src=\""+bookIcon+"\"  alt=\"image\" />\n" +
        "                <div class=\"product_info\">\n" +
        "                \t<p>"+bookInfo+"</p>\n" +
        "                 <div class=\"Buy_book\"><a href=\""+bookLink+"\">Read</a>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "                <div class=\"cleaner\">&nbsp;</div>\n" +
        "            </div>\n" +
        "\n" +
        "            <div class=\"cleaner_with_width\">&nbsp;</div>";
    document.getElementById('bookPlaceHolder').innerHTML=bookHTML;
}



function generateSQL(bookName,bookAuthor,bookInfo,bookLink,bookIcon)
{
    var sql="INSERT INTO `book_db` (`ID`, `name`, `author`, `info`, `link`, `icon`, `price`) VALUES (NULL, '"+bookName+"', '"+bookAuthor+"', '"+bookInfo+"', '"+bookLink+"', '"+bookIcon+"', '200');"
    console.log(sql);
}