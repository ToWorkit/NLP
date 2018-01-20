const puppeteer = require('puppeteer');
var child_process = require('child_process');
var fs = require('fs')
let axios = require('axios')
let qs = require('qs')

function sleep(second) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(' enough sleep~');
        }, second);
    })
}

var arguments = process.argv.splice(2);
// console.log(arguments)
var book_id = `${arguments[0]}`
var url = `http://t.shuqi.com/route.php?pagename=route.php#!/ct/cover/bid/${book_id}`
var promotion_type = arguments[1]

class Parse {
  constructor() {
    this.page = null
    this.browser = null
    this.chapterParamsConent = null
  }
  async init() {
    // 是否显示浏览器
    this.browser = await puppeteer.launch({
      'headless': false,
      // 'executablePath': 'C:/Users/hedy/AppData/Local/Google/Chrome/Application/chrome.exe'
    });
    // 等待页面打开
    this.page = await this.browser.newPage();
    // 设置信息
    const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
    await Promise.all([
        this.page.setUserAgent(UA),
        this.page.setJavaScriptEnabled(true),
        this.page.setViewport({width: 1100, height: 1080}),
    ]);
    // 章节内容
    this.getChapter()
    // 图书信息
    // this.getBook()
  }
  // 获取图书信息
  async getBook() {
    await this.page.goto(url);
    let page = await this.page
    // console.log(page)
    // 获取请求完成的信息
    page.on('requestfinished', request => {
      if (request.resourceType == "xhr") {
        // console.log(request.method);
        if (request.method == "POST") {
          // console.log(request.postData);
        }
        if(request.url.indexOf('http://walden1.shuqireader.com/webapi/book/info') != -1) {
          (async () => {
            let res = await request.response()
            let result = await res.json();
            let res_data = result.data
            // 单本图书详情
            let bookMessage = {
              'book_id': res_data.bookId,
              'book_name': res_data.bookName,
              'book_summary': res_data.desc,
              'book_end_status': res_data.state,
              'book_keywords': res_data.tag[0].tagName ? res_data.tag[0].tagName : null,
              'author_name': res_data.cpName,
              'cover_url': res_data.imgUrl,
              "book_is_vip": res_data.payMode,
              "book_published_time": 0,
              'book_update_time': res_data.lastInsTime
            }
            // console.log(await bookMessage)
            const put_book = params => axios.post(`http://192.168.0.126:8011/v1.0/other/book_info`,  qs.stringify(params))
            put_book(await bookMessage).then( async (res) => {
              if (res.data.code == 200) {
                console.log(res.data.code)
                await this.browser.close();
              }
            }).catch(err => {
              console.log(err)
            })
            // let result = await res.text();
            //  const chapter_list = await page.$eval('#page-chapter-list', el => el.innerText);
            //   console.log(chapter_list);
          })()
        }
      }
    });
  }
  // 章节信息
  async getChapter() {
    let chapter_url = `http://t.shuqi.com/route.php?#!/ct/chapterList/bid/${book_id}`
    await this.page.goto(chapter_url);
    let page = await this.page
    // 获取请求完成的信息
    page.on('requestfinished', request => {
      if (request.resourceType == "xhr") {
        // console.log(request.method);
        
        if (request.method == "POST") {
          // console.log(request.postData);
        }
        if(request.url.indexOf('http://walden1.shuqireader.com/webapi/book/chapterlist') != -1) {
          (async () => {
            let res = await request.response()
            let result = await res.json();
            let chapter_list = result.data.chapterList
            // 单本图书详情
            for (var i in await chapter_list) {
              // 可能会有卷 -> []
              for (var item in chapter_list[i]) {
                if (item == 'volumeList') {
                  // 章
                  for(var only in chapter_list[i][item]) {
                      // 是否显示浏览器
                      let _browser = await puppeteer.launch({
                        'headless': false,
                        // 'executablePath': 'C:/Users/hedy/AppData/Local/Google/Chrome/Application/chrome.exe'
                      });
                      // 等待页面打开
                      let _page = await _browser.newPage();
                      // 设置信息
                      const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
                      await Promise.all([
                          _page.setUserAgent(UA),
                          _page.setJavaScriptEnabled(true),
                          _page.setViewport({width: 1100, height: 1080}),
                      ]);
                      let chapter_url_ = `http://t.shuqi.com/route.php?#!/ct/read/bid/${book_id}/cid/${chapter_list[i][item][only].chapterId}/ct/read`
                      // console.log(chapter_url_)
                      // await sleep(5000)
                      // 获取请求完成的信息
                      _page.on('requestfinished', request_ => {
                        if (request_.resourceType == "xhr") {
                          if (request_.method == "GET") {
                            (async () => {
                              let res_ = await request_.response()
                              let result_ = await res_.json();
                              this.chapterParamsConent = {
                                'channel_book_id': book_id,
                                'chapter_id': chapter_list[i][item][only].chapterId,
                                'chapter_content': null,
                                'chapter_name': chapter_list[i][item][only].chapterName,
                                'chapter_order_number': chapter_list[i][item][only].chapterOrdid,
                                'chapter_published_time': chapter_list[i][item][only].chapterUpdateTime,
                                'chapter_last_update_time':chapter_list[i][item][only].chapterUpdateTime,
                                'chapter_need_pay': chapter_list[i][item][only].payStatus,
                                'promotion_type': promotion_type
                              }
                              // console.log(await chapterParamsConent)
/*                              fs.appendFile('./message.txt', await JSON.stringify(chapterParamsConent),function(err){
                                  if(err) console.log('写文件操作失败');
                                  else console.log('写文件操作成功');
                              });*/
                            })()
                          }
                        }
                      })
                      await sleep(5000)
                      await _page.goto(chapter_url_);
                      await sleep(1000)
                      // await _browser.close()
                      _page.mainFrame().waitForSelector('#read_in > div.read-main > div.read-body > div:nth-child(1) > p:nth-child(4)').then(async () => {
                        let page_content = await _page.$eval('#read_in div.read-main div.read-body', el => el.innerText);
                        try{
                          let buy_content = await _page.$eval('#buy-btn', el => el.innerText);
                          if (buy_content) {
                            (async () => {
                              await _browser.close();
                              return
                            })()
                          }
                        }finally{
                          // console.log(await this.chapterParamsConent)
                          let params_chapter = await this.chapterParamsConent
                          params_chapter.chapter_content = await page_content
                          await sleep(2000)
                          const put_chapter = params => axios.post(`http://192.168.0.126:8011/v1.0/other/chapter_info`,  qs.stringify(params))
                          console.log(await params_chapter)
                          put_chapter(await params_chapter).then( async (res) => {
                            if (res.data.code == 200) {
                              console.log(200)
                              await _browser.close();
                            }
                          }).catch(err => {
                            console.log(err)
                          })
                        }
                      })
                  }
                }
              }
            }
            // await this.browser.close();
            // let result = await res.text();
            // const chapter_list = await page.$eval('#page-chapter-list .chapter-list', el => el.innerText);
            // console.log(chapter_list);
          })()
        }
      }
    });
  }
}

let parse = new Parse()
parse.init()
