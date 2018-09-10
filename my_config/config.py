save_path = '/home/python/pic_spy/albums'
log_path = '/home/python/pic_spy/logs'
artist_list = {
    '362174':'https://jiran.tuchong.com',
    '1177577':'https://gongzichangan.tuchong.com',
    '1186455':'https://deer-vision.tuchong.com',
    '1446952':'https://pengpengdalizi.tuchong.com',
    '1324421':'https://linyi1311.tuchong.com',
    '1790610':'https://sue0722.tuchong.com',
    '1145421': 'https://tuchong.com',
    '354368': 'https://hiseephoto.tuchong.com',
    '990878': 'https://lucici.tuchong.com',
    '1136739': 'https://tuchong.com',
    '344025':'https://atlantis0428.tuchong.com',
    '1342351':'https://fire-3.tuchong.com',
    '1139811':'https://tuchong.com',
    '363331':'https://sixfs.tuchong.com',
    #'279640':'https://onexiang.tuchong.com',
    '1037985':'https://sushiyi.tuchong.com',
    '515209':'https://tuchong.com',
    '388420':'https://zwyoyi.tuchong.com',
    '340244':'https://tuchong.com',
    '65403':'https://eale.tuchong.com',
    '1030308':'https://lanhai.tuchong.com',
    '1287992':'https://shenan.tuchong.com',
    '1178344':'https://sugarin.tuchong.com',
    '280988':'https://azeros.tuchong.com',
    '243731':'https://jasonzou.tuchong.com',
    '53023':'https://secret.tuchong.com',
    '336885':'https://tuchong.com',
    '445081':'https://tuchong.com',
    '1107056':'https://tuchong.com',
    '275736':'https://suyi.tuchong.com',
    '1314529':'https://tuchong.com',
    '1064195':'https://daddy.tuchong.com',
    '1046081':'https://tuchong.com',
    '3326940':'https://3photography.tuchong.com',
    '1332533':'https://tuchong.com',
    '288782':'https://littledemon.tuchong.com',
    '1039253':'https://tuchong.com',
    '3505293':'https://tuchong.com',
    '3522380':'https://tuchong.com',
    '1745920':'https://tuchong.com',
    '2934511':'https://tuchong.com',
    '352764':'https://wxtx.tuchong.com',
    #'515209':'https://tuchong.com'#星岚
}

poco_account_ids = {
    #http://www.poco.cn/user/user_center?user_id=56546987
    	#'174574302':{'author':'尘埃微凉', 'code':['f2a37d9659d2fb48085', '70b8e84ed9f4a4cfdd0', '965440ba2146632ecf0', '4dc3cc1d71481512d86', 'af0475c24f1370bf9f0', '860cf824d7aa9027131', 'b76ac47022c3c267597', '559f115db71e776906a']},#尘埃微凉
    	'174572931':{'author':'疯子', 'code':['406ef59705efb4e425f', '8095dbcde5d8895617c', 'b6645eac530c2e8c1fe', '77bd2d42922eea21144', '1130a3dc61ae1a7d82e', '9edf58ccdc4dd86d2a1', '68bec63599ffcad6a23', 'de1769c2d20f85c6751', '89a97bed3c11bb6d6ca', 'c1efc995b9596a41237', '2ead63a548b01177951', 'fb8bf7213b671fa226f', 'be4bcbbe276602ce68f']},#疯子
    	'177176218':'9229061252cccadb18f',
    	'3417570':{'author':'Gyeonlee', 'code':['ced79f0568fa7cadaa1', '23dd9c3c6ad09217ff1', 'b290ca49dc42cd63ae3', '60069256976e082e988', 'd99b46b662f780381f1', '3d721c365b19e5279e1', '2b358480c9de7d04f75', '6731a7290fc9f1588d7', 'd2adef62994b44316e8', '72c56731420f9d2691b', '1d39a4e128aa8399030', '3d53a85b9f766ae8629', '92439ab89a93ff3b8cd']},
    	'173636313':{'author':'独立摄影师石头', 'code':['ff762eefdedf489a139', '681d2a4a6bb6eca43f0', '82dc0bf4ea0305bb125', '1251c66debb9ac60e44']},
    	'66096257':{'author':'青研映画', 'code':['233dd86022ee4abfad1', 'a1ddb491d7890648275', '326d90aa2bf06c9d59a', 'ded8b92a87ae6f97acb', '6be21f33c4b4c9baddc','9a44611ddba11c2c619']},
    	'173388816':'6b5b2f8292b593118ad',
    	'174848104':'3e1daaec63f772edfcc',
    	'185652848':'8e39023858be8d32e21',
    	'200513958':'77c2259120872addd25',
    	'63443172':'35aa80b13d3ad3d5d4e',
    	'178957211':{'author':'小麦Skin', 'code':['5575cdfba172fd87a46', '0e72706ee18bf5ebb93', 'b1757350c223e203435', 'b2b234c832eacbdc6c5', '0e55cb42dd1f0324dad']},#
    	'64206635':{'author':'花想衣裳', 'code':['769330cd015770794d7', 'd10bfca19e9763dab5c', 'd3e18eac25f15ec2a67', 'dcbe2ca976c23d3d956', 'e90324bfe5d7b0c17b1']},
    	'174079515':'3f24a5c860313797d4d',
    	'19430718':'0ce08eed59bd0cef426',
    	'67593620':'054a8f14068e0c51998',
    	'3417570':'ced79f0568fa7cadaa1',
    	'174730832':{'author':'云浮木', 'code':['90d1fe0c81a11a1f17c',  'eaeeea2a54dabd5639a', 'ad1292e236f37eaa7f1','b62b4a3892d44aeccf0','34e32c8d9c33688cf93']},#云浮木
    	'66546564':'1177c50fe7622b99154',
        '56546987':'56348c417ff0b182d1f',#城子
        '1242841':'85e8bb8eb5fb4528284',
        '174574453':{'author':'知竹zZ', 'code':['c5c57f81b141a804b92', '17c6be737559da73b38', '4aa87b0a2f57d6dae0f','cf880d59b713ddd8081','2495218bceac5a58959','f36bb002bff4d6b1b38']},
        '66431972':'841262702a1b4ce4183',
        '56509843':'11f3121c62dfc768da3',
        '174316516':'2a9836876849fa80820',
        '57837318':'6da5df91945bf9bc3e5',
        '52367905':'88806287fd63c6159e1',
        '52967121':'7c3e4024ef8c3c8223a',
        '44988233':'01d974a5aa0638ae88e',
        '173636313':'ff762eefdedf489a139',
        '51955220':'850166acf1e16e9de87',
        '178265607':'649c119e39029ba65cc',
        '179593166':'284acce00d1dfd74c75',
        '55708170':['0f1e7705e06c9cc75de', '9b337c5c595ed4ccedb'],
        '56551348':['c4dd608c974df605d71','a2f24b32ddc5210dbd2','dcb61ee03db793cac37','92bb2f73684400ba836','145ee1529af2aeeea93','70b76885dae2d9522a8'],
        '53868931':['193a046f93f41798590', 'a46cf5bd0f344d393be', '43d21bc921643cf2d7e','685a6a413b1efc6b052', '0cf8bce34b0f3f52ba6', 'ead8fe2a0a50ae3ca23', '61d9a711e4a46784360', 'fc763a4e4ec4a161d70', '9c4cf7f453a5d0d5222'],
        '52812329':['a3d074229bff7e394fc', '14bd90a69d14fdf4e1a', 'a35d500bfd087f5fdf0', '5dd584913f922d0e02e', '5a254cd2ffb18cbd67a', 'ad34db66f0e4a6c8583', '9804d7e5e6e00968886', '8e61beb3da96b3eb2ce', '86ca7f6cbaf26c74b6c', 'd4803edeed8ec17466c'],#拾壹-MLZZ
        '51802661':['81f281af758a9a588c1', 'e55614aa3e70ea790d3', '4377d333e5ecef28433','6072e02d71f6364d2cb', '0d83b63e377dd1dc00e','5ab2032c2fc7264c581'],#西瓜
        '56470991':['1c498e69efd2df243bb','a37c4e63457a56ed6e1','5012d04e32fe026d737','5bd1232b710983f1752'],
        '64316077':['6a56efd6639264418eb','74e623068ff12081f18', '1501e64a976ec6cb7c8'],
        '184030735':['67fe33692c8d857642f','a499469047664a9f1b5'],
        #'173403228':['e62865161d963f2dd47','00ef862b415f7f620f8'],
        '178916997':['7ae2485a1b6c750ccd8', '9b815175f73b3ed4976'],
        '1242841':{'author':'清江水', 'code':['85e8bb8eb5fb4528284','02ba587be4c69bafdae', 'b5259efb870f2610c5f', 'cfe2a631760d9a5775f', '1a77bd2a0fb9757aa86', 'b671e8477bdc1cda4a3', 'ec8b9f619adce076335', 'e6836cb07a6831a1e32', '', '']},
        '175266669':{'author':'喵小姐','code':['a35902d432e52c1d3e4', '5f7bc5014326f03d61e', 'd5e3b38ad7547bbcf85', 'ff8534a8c277b9fb156', '3c919177591492bd10a', '1e48c35fa23fa013c7b', '2f06cff70e3e6af1203', '436669e4714e4bc7979', '0d7e6edc72b5e541e20', '40f16057e0524fed8be', '4a77a81b58d2c0f1479', '881e805e7f751243187', '788d84bf46806d4951e', '454d0df69205bc43933', '6fe97582651a188138c', '485d4451ac80bab933b', 'e14ba45ec245a45e389', '56792e2678c22ddaa04', '26a3be8219e161879c9', 'ba68757f7fa6526dbe7']},
        '54977030':{'author':'caocaofactory','code':['83040829211f3a3df3f', '9055ba1c4a28d1a2a29', 'a787a9cd2fd440a829c', 'c3d6514ced7e0094fd7', '37849477de72011e7e7', 'df7a47ab47bae087c2c', 'b1ea1b518d66ecc40c6']},
        '56509843':{'author':'人称阿坤','code':['11f3121c62dfc768da3', '0632f3dbfb8f9ea3f0b', '046692c466ab5ee5ac5', '0ce86f05131e26194b0', '74dd9da41110b15fc02']},        
        #'174649232':{'author':'六指卫星', 'code':['ab7011989d0ead0acec', '4bd9bd434cead406494', 'b1cdf35db4e6ea6ef81', '6ad88f1596773af6eb0', '4c56785b79da3046bcb', 'da92cce5952c97db97a', '6b4dfb6ecbb3d4675ef']},#六指卫星
        #'21595018':{'author':'行色匆匆', 'code':['080df7726fc8d162b97', '557117aa7338ac78587', '0f66334da9ee75c29d8', '37314d88487a3ee9256', 'd4ca19cd042627db53e', 'bc5001307e64e6b3efc']},#行色匆匆
        '53423058':{'author':'阿浩photo', 'code':['25eee2553b3aa36665a', '8f9d66f60e7ae0d975c','964c33d735ea07b5981', '1c469c321f42e75471c', 'd6464610dbc438ced23', '53231a459a569e85171']},#阿浩photo
        '51890960':{'author':'星岚', 'code':['3e01dfbaf78ce24f361', 'd583b3aec9656f86592', 'a493ac187c6f1507e2e', '84f345db0d4d7cb6202', '4baf4143e53f078a902', 'a202074a8f6623529d6', 'b11825abcd3492a19bf', '07e75c4fbc4a26e628f', '0304ced1d72b1ed0969', '78ee724ebe1775ee9a9', '93ef7857678a9ad8b63', '93f667a557ec5b6f77c', '39d0278d2e52db4530b', 'b4a97066457b67cf263', '77248582c44cf47e8ff']},#星岚
        '44298285':{'author':'蓝色贝壳', 'code':['cf8092c5eec564fbc47', '86f53793d881d4305ee', '1d996be743f20fd59cd', '02cc6566916f252fd34', '04f16e0bd318f254d5e', '06ea3b0f53d815e8636']},
        '54865205':{'author':'清欢', 'code':['7fa00b3049e22c644af', '4c5d65a33409c2afbb0', '86f53793d881d4305ee', '1d996be743f20fd59cd', '02cc6566916f252fd34', '04f16e0bd318f254d5e', '06ea3b0f53d815e8636']},#清欢
        '52515975':{'author':'七七小姑凉', 'code':['877c375b1f78e1c1e4e', '8d9c0ff8b5474f081ac', '1e873c754d63c4520c0', '9542056a7972b6a7285', 'f8eb7218782dfe69fe8','55db85b89648ba851a2', '42e78d76ed7096aa070', '045240f8dab39b91657', 'cf9269ddac69f9b36ee']},#七七小姑凉
        '55322527':{'author':'老威威', 'code':['5e93e1290df4702ab69', '1e47698d6db903a8e6f','6d4183bf5f240cf95e9', '885512256a700bcb875','11cb522c7192e24e555', '1c4d2ae92e7a6195de1','511fb0d8e6cf3875506', '188c246f189b352b74e','d629685382727017bc0', 'bf439891b652b89381b','bbf8f65ade799ffbe51']},#老威威
        #'34644156':{'author':'阳晨波', 'code':['b23290d8c2f44571b89', 'f9b882e4d6e23d5bdbc', 'c458ce3d30d2ee66ec1','cf65e11bd35ed168b37','a9c16b26197de8fdcdc', 'be9bde7f80c210c000b', '3f8cdacf94671b91361', '828872f50fd704842f1','8f546db7f9057510fbc','302a73470bd517e1bca','6f0330e0e66c179a12c']},#阳晨波
        '52947828':{'author':'柔7', 'code':['2bc64016941d45b4350', '95726add2f7d26fdac6', '4c8fcbaebad5e7ce15e', '848b6431251ebff7359', '4d72e09f7aa4d99aed7', '9fbf70b801664c4ec19','b2b8727754fb515e558','7363bcf45b094ab2197', 'a4cb3813d11bca00213','e03ffcf9e4726f21980', '0bad52809d55ca4262e','55430eef9dbaaec39b1', '9c77624c7d9397613c0', '893b002fca3e5eba980', 'f47a20efae3e0330f93', '5305a370cb30081907c','e95b6dfdd22dc3c8386']},#柔7
        '174413193':{'author':'微醺十月', 'code':['0a7b1ac49e197a2730c', '2d40ce21f3bfaffc0c5', 'f74af9c4ec46e9f73f2', 'c93b3fbe3ffb38085f2', '7d18abacaf0975d9c3b', 'c09eeb4f7845393a62d', 'a2d27ef1c29475af2e4', 'f6ffc62381b7830561d', '09615a9e4a9a4ba5801']},#微醺
        '43324521':{'author':'格式化', 'code':['381cece374f92168968', '8dc14f147527b786c69', '6dffbb8e1e2ace70bb1', 'd651ece1f2fed9b9cdb', 'd6e2e2360bd2f0edcd4', 'f8105911ed0b19cb606', '438166aab0b657c345a', '70aa5efeecaee17b1b4', '3a8a614fb85ffc58bef', 'e1ee8fe833271702bf8']},#格式化
        #'173726994':{'author':'luna_atlantis', 'code':['c17e18e5906987a1a37','f0e35d1f614b4048bb5', '9c9e21b60e0c1b24c49','e651865217b87793924', 'edad2eadc9a3131b2d9','7ccc309cb566b7ff882','756699e8f2e1801b580','1a9ebd5b04ef8ecd2e9','2533dce3f2dd1a39486','3c3150ad3f68a02718b','ecaf919a314035834da','a76b7b53a5364b66f55']}#luna
}

tpy_blog_urls = [
    'http://dp.pconline.com.cn/8806083',
    'http://dp.pconline.com.cn/33941406',
    'http://dp.pconline.com.cn/8640908,'
    'http://dp.pconline.com.cn/31891740',
    'http://dp.pconline.com.cn/34394448',
    'http://dp.pconline.com.cn/15660510',
    'http://dp.pconline.com.cn/45106808',
    'http://dp.pconline.com.cn/8565706'
]

five_hundred_artist_list = [
    'https://500px.com/redbug',
    'https://500px.com/eikonas',
    'https://500px.com/markcrislip',
    'https://500px.com/kordan',
    'https://500px.com/warrenkeelan',
    'https://500px.com/subiyama',
    'https://500px.com/fl-photostudio',
    'https://500px.com/michaelschnabl',
    'https://500px.com/ivankopchenov',
    'https://500px.com/crescenzov2',
    'https://500px.com/diverstef',
    'https://500px.com/hengki24',
    'https://500px.com/carman-uk',
    'https://500px.com/fxkito2',
    'https://500px.com/diverstef',
    'https://500px.com/marconunofaria',
    'https://500px.com/brockwayout'
]

xiami_config = {
    'uid':'10425939',
    'email':'gw655@126.com',
    'password':'',
    'login_url':'https://login.xiami.com/web/login',
    'logout_url':'http://www.xiami.com/member/logout?from=mobile',
    'collection_url':'https://www.xiami.com/space/lib-song/u/[uid]/page/[page]',
    'song_info_url':'http://www.xiami.com/widget/xml-single/uid/0/sid/[sid]'
}

xiami_collection = {
    'next_page_url':'https://www.xiami.com/collect/ajax-get-list?id=[id]&p=[page]&limit=[page_size]',
    'set_pos_url':'https://www.xiami.com/collect/ajax-update-song',
    'max_page_size':50,
    'list':[
        #'https://www.xiami.com/collect/15176924',
        #'https://www.xiami.com/collect/120123323',
        #'https://www.xiami.com/collect/413114513',
        'https://www.xiami.com/collect/413114513'
    ]
}

lofter_blogs = [
    {'home':'http://linxiaoyisheying.lofter.com', 'img_pattern':'.box .pic a::attr(bigimgsrc)'},
    {'home':'http://mmmaybe.lofter.com','img_pattern':'.box .pic a::attr(bigimgsrc)'},
    {'home':'http://seewyn.lofter.com','img_pattern':'.content .wrap .img a::attr(bigimgsrc)'},
    {'home':'http://terryfengphotography.lofter.com','img_pattern':''},
    {'home':'http://misssecret.lofter.com','img_pattern':''},
    #{'home':'http://fire-3.lofter.com','img_pattern':''},
    {'home':'http://lingwkr.lofter.com','img_pattern':''},#害羞的樱桃
    #{'home':'http://shenan99.lofter.com','img_pattern':'.box .pic a::attr(bigimgsrc)'},
    {'home':'http://onexiang.lofter.com','img_pattern':'.box .pic a::attr(bigimgsrc)'},
    #{'home':'http://yfmphoto.lofter.com','img_pattern':'.box .pic a::attr(bigimgsrc)'},
    #{'home':'http://wuxiantx.lofter.com','img_pattern':'.post .postphoto a::attr(bigimgsrc)'},
    {'home':'http://imulin.lofter.com','img_pattern':'.main .content .img a::attr(bigimgsrc)'},
    {'home':'http://linchuhan.lofter.com','img_pattern':'.cont .pic .img a::attr(bigimgsrc)'},
    #{'home':'http://sixfs.lofter.com','img_pattern':'.cont .pic .img a::attr(bigimgsrc)'},
    {'home':'http://dingxiaoning.lofter.com','img_pattern':'.detail-ct .box .pic a::attr(bigimgsrc)'},
    {'home':'http://zuoxiaohong.lofter.com','img_pattern':'.box .pic a::attr(bigimgsrc)'},
    #{'home':'http://azeros.lofter.com','img_pattern':'.ct .pics .pic a::attr(bigimgsrc)'},
    {'home':'http://fz-photography.lofter.com', 'img_pattern':'.content .wrap .img a::attr(bigimgsrc)'},
    {'home':'http://coculiu.lofter.com', 'img_pattern':''},
    {'home':'http://coolmoonflower.lofter.com', 'img_pattern':'.post-ct .box .pic a::attr(bigimgsrc)'},
    {'home':'http://luckytoto.lofter.com', 'img_pattern':''},
    {'home':'http://kite-vison.lofter.com', 'img_pattern':''},
    {'home':'http://octopus-d.lofter.com'},
    {'home':'http://hellomaozexi.lofter.com', 'img_pattern':'.main .content .img a::attr(bigimgsrc)'},
    {'home':'http://fangtse.lofter.com', 'img_pattern':'.content .wrap .img a::attr(bigimgsrc)'},
    {'home':'http://honghan-studio.lofter.com', 'img_pattern':''},
    #{'home':'http://laoweiwei.lofter.com', 'img_pattern':''},
    {'home':'http://beidaoweibei.lofter.com', 'img_pattern':'.photowrapper .imgwrapper a::attr(bigimgsrc)'},
    {'home':'http://zhangshaozeng.lofter.com', 'img_pattern':'.main .content .img a::attr(bigimgsrc)'},
    {'home':'http://rickywu.lofter.com'},#追风的瑞恩
    {'home':'http://youshijuesheyingguanfangweibo.lofter.com'},#右视角
    {'home':'http://ealelaomi.lofter.com', 'img_pattern':'.photowrapper .imgwrapper a::attr(bigimgsrc)'}, #右视角老秘
    {'home':'http://aaronsky.lofter.com'},
    #{'home':'http://xuewy.lofter.com'}#七七小姑凉
]

