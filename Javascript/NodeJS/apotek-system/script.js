

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
(async () => {
    
    const puppeteer = require('puppeteer');
    const fs = require('fs');
    
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await scrapeApotek1(page, fs, "https://www.apotek1.no/produkter", "vitamin", true);
    
    // await scrapeVitusApotek(page, "https://www.vitusapotek.no", "", false);
    
    
    
    
    await browser.close();
})();

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
async function scrapeApotek1(page, fs, url, query, addScreenshot) {
    
    await page.goto(url);
    
    const [searchField] = await page.$x('//*[@id="site-search-input"]');
    await searchField.type(query);
    await searchField.press('Enter');

    const [searchButton] = await page.$x('/html/body/app-root/main/mat-sidenav-container/mat-sidenav-content/a1-components-header/mat-toolbar/div[3]/div[1]/div[1]/button');
    searchButton.click();

    const [cookies] = await page.$x('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll"]');
    cookies.click();
    await delay(2000);

    const [htmlResults] = await page.$x('/html/body/app-root/main/mat-sidenav-container/mat-sidenav-content/app-catalog-search-page/b2c-product-search-list/mat-sidenav-container/mat-sidenav-content/a1-components-product-grid');
    const articles = await htmlResults.$$('article');
    console.log(articles.length);

    // // Loads more items onto the web-page
    // for (let i = 0; i < 5; i++) {
    //     const [more] = await page.$x('//*[@id="load-more"]');
    //     await more.click();
    //     await delay(2000);
    // }

    for (let i = 0; i < articles.length; i++) {

        const item = await articles[i].evaluate(x => x.firstChild.firstChild.childNodes[1].firstChild.childNodes[2].textContent, htmlResults);
        console.log(item);

        if (addScreenshot === true) {
           
            const path = "data/" + query;
            
            fs.access("./" + path, (error) => {
                if (error) {
                    fs.mkdir(path, (error) => {
                        if (!error) console.log("New folder!");
                        else console.log(error);
                    });
                }
            });
            
            await articles[i].screenshot({ path: path + "/" + item + ".png" });
        }
    }
    
    // testing stuff
    // const txt = await idk.getProperty('textContent');
    // const rawTxt = await txt.jsonValue();
    // console.log(rawTxt, "\n");
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
async function scrapeVitusApotek(page, url) {
    
    await page.goto(url);
    
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function delay(time) {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}