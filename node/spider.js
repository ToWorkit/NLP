/**
 * 请求接口的方式获取数据
 */

let request = require('request')
let express = require('express')
let axios = require('axios')
let qs = require('qs')
let app = express()
var child_process = require('child_process');
axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;

// 接收参数 node spider.js <参数>
var arguments = process.argv.splice(2);
console.log(arguments)
// child_process.exit(0)

let params = {
  'id': `${arguments}`
}

// var chapterParams = {}

const getWy = params => {return axios.get(`https://yuedu.163.com/getBook.do?id=${arguments}&tradeId=`, {params: params}).then(res => res.data)}

class Parse {
  constructor() {
    this.res = null
    this.count_ = 0
  }
  async init() {
    this.putBook()
  }
  // 获取图书信息
  async getBook() {
    return new Promise((resolve, reject) => {
      getWy(params).then(res => {
        this.res = res
        // 单本图书详情
        let bookMessage = {
          'book_id': res.id,
          'book_name': res.title,
          'book_summary': res.shareDescription,
          'book_end_status': res.state,
          'book_keywords': res.tags ? res.tags : null,
          'author_name': res.author,
          'cover_url': res.coverImg,
          "book_is_vip": 0,
          "book_published_time": 0,
          'book_update_time': Math.ceil(res.updateTime / 1000),
        }
        resolve(bookMessage)
      })
    })
  }
  // 获取章节内容所需参数
  async getChapterParams() {
    // 书籍信息
    let book =  await this.getBook()
    let res = await this.res
    // 章节参数
    let chapterParams = []
    for (var item in res.portions) {
      let items = {
        'articleUuid': res.portions[item].id, // 书籍id
        'bigContentId': res.portions[item].bigContentId
      }
      chapterParams.push(items)
    }
    return chapterParams
  }
  putChapterCon(params) {
    // console.log(params)
    const put_chapter = params => axios.post(`http://192.168.0.126:8011/v1.0/other/chapter_info`,  qs.stringify(params))
    put_chapter(params).then(res => {
      console.log(res.data.code, this.count_++)
    }).catch(err => {
      console.log(this.count_)
    })
  }


  // 请求章节内容
  async getChapterCon_(i) {
    let chapterParams_ = await this.getChapterParams()
    let res = await this.res
    let sourceUuid = res.id
    // 章节
    let chapterList = res.portions
    // 章节计数
    const getChapterCon = params => {return axios.get(`https://yuedu.163.com/getArticleContent.do?sourceUuid=${sourceUuid}&articleUuid=${chapterParams_[i]['articleUuid']}&bigContentId=${chapterParams_[i]['bigContentId']}`).then(res => res.data)}
    // 每章
    let itemChapterCon = await new Promise((resolve, reject) => {
        getChapterCon().then(res => {
          resolve(res)
        })
    })
    console.log(await itemChapterCon)
    let time_ = Math.ceil(new Date().getTime() / 1000)
    if (res.id && chapterList[i]['id'] && await itemChapterCon['content'] && await chapterList[i]['title']) {
      console.log('<--->', this.count_)
        // 传递数据
        var chapterParamsConent = {
          'channel_book_id': res.id,
          'chapter_id': chapterList[i]['id'],
          'chapter_content': await itemChapterCon['content'],
          'chapter_name': await chapterList[i]['title'],
          'chapter_order_number': ++this.count_,
          'chapter_published_time': time_,
          'chapter_last_update_time':time_,
          'chapter_need_pay': chapterList[i]['needPay']
        }
        const put_chapter = params => axios.post(`http://192.168.0.126:8011/v1.0/other/chapter_info`,  qs.stringify(chapterParamsConent))
        put_chapter(params).then(res => {
          if (res.data.code) {
            if (i >= chapterParams_.length) {
              return
            }
            ++i
            this.getChapterCon_(i)
          }
        }).catch(err => {
          // console.log(err)
          console.log(this.count_)
        })
    }
  }
  // 传输数据
  // 书籍信息
  async putBook() {
    let params = await this.getBook()
    console.log(params)
    const put_book = params => axios.post(`http://192.168.0.126:8011/v1.0/other/book_info`,  qs.stringify(params))
    put_book(params).then(res => {
      if (res.data.code == 200) {
        // console.log(1)
        this.getChapterCon_(0)
      }
    }).catch(err => {
      console.log(err)
    })
  }
}

let parse = new Parse()
// parse.getBook().then(res => {
//   console.log(res)
// })
// parse.getChapterCon_(0)
parse.init()
