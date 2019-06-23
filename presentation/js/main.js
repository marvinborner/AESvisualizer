let currentTable = 0;

function createTable(selector, hex) {
    let parent = document.getElementById(selector);
    let decription = document.querySelector("#" + selector + " small");
    let matrix = decription.textContent;
    let table = document.getElementsByClassName("tableTemplate")[0].cloneNode(true);
    let delimiter = hex ? " " : "";

    table.setAttribute("id", "table" + currentTable);
    parent.insertBefore(table, decription);
    for (let i = 0; i < 16; i++) {
        document.querySelector("#table" + currentTable + " [data-id='" + i.toString() + "']")
            .innerText = matrix.split(delimiter)[i] !== undefined ? matrix.split(delimiter)[i] : "01"
    }
    currentTable++;
}

createTable("AES_1");
createTable("AES_2");
createTable("AES_3", true);
createTable("AES_4", true);
createTable("AES_5", true);
createTable("AES_6");
createTable("AES_7", true);
createTable("AES_8", true);
createTable("AES_9", true);
createTable("AES_10", true);
createTable("AES_11", true);
createTable("AES_12", true);
createTable("AES_13", true);
createTable("AES_14", true);
createTable("AES_15", true);
createTable("AES_16", true);
createTable("AES_17", true);
