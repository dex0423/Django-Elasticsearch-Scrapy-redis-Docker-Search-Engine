from elasticsearch_dsl import Document, Nested, Date, Boolean, analyzer, Completion, Text, Keyword, Integer, Double
from elasticsearch_dsl.connections import connections

# 新建 ES 连接
connections.create_connection(hosts=['localhost'])

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


class Customanalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = Customanalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(Document):

    # 推荐 & 自动补全
    suggest = Completion(ik_analyzer)

    # 项目名称
    project_name            = Text(analyzer="ik_max_word")              # 需要进行分词搜索
    # 项目坐落
    position                = Text(analyzer="ik_max_word")
    # 预售证号
    presale                 = Keyword()                                 # 不需要分词搜索，全量保存
    # 预售面积
    presale_area            = Double()
    # 预售套数
    presale_num             = Integer()
    # 批准时间
    permit_date             = Date()
    # 建筑设计单位
    constrution_designer    = Text(analyzer="ik_max_word")
    # 环艺设计单位
    green_designer          = Text(analyzer="ik_max_word")
    # 土地地块号
    land_number             = Keyword()
    # 投资立项批准号
    invest_permit           = Keyword()
    # 土地出让合同号
    land_transfer_contract  = Keyword()
    # 土地取得方式
    get_land_method         = Keyword()
    # 土地面积
    land_area               = Double()
    # 土地使用年限
    land_use_expiration     = Keyword()
    # 土地规划用途
    land_usage              = Keyword()
    # 土地作用起始日期
    land_startdate          = Date()
    # 土地作用结束日期
    land_finishdate         = Date()
    # 技术经济指标
    tech_ecno_index         = Keyword()
    # 容积率
    plot_ratio              = Double()
    # 绿化率
    green_ratio             = Double()
    # 车位数
    parking_num             = Double()
    # 交付标准
    delivery_require        = Keyword()
    # 周边环境
    position_enviroment     = Text(analyzer="ik_max_word")
    # 配套设施
    corollary_facility      = Text(analyzer="ik_max_word")

    presale_url             = Keyword()
    presale_url_object_id   = Keyword()

    # 爬取时间
    crawl_time              = Date()


    class Index:
        name = "luanyushou"
        settings = {
          "number_of_shards": 5,
        }

    # class Meta:
    #     index = "luanxinfang"
    #     doc_type = "article"


if __name__ == '__main__':
    ArticleType.init()
