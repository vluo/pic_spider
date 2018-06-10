import os, sys
import json
import  hashlib
import execjs

js ='''
	function r(n, t) {
		var r = (65535 & n) + (65535 & t),
			e = (n >> 16) + (t >> 16) + (r >> 16);
		return e << 16 | 65535 & r
	}
	function e(n, t) {
		return n << t | n >>> 32 - t
	}
	function u(n, t, u, o, c, f) {
		return r(e(r(r(t, n), r(o, f)), c), u)
	}
	function o(n, t, r, e, o, c, f) {
		return u(t & r | ~t & e, n, t, o, c, f)
	}
	function c(n, t, r, e, o, c, f) {
		return u(t & e | r & ~e, n, t, o, c, f)
	}
	function f(n, t, r, e, o, c, f) {
		return u(t ^ r ^ e, n, t, o, c, f)
	}
	function i(n, t, r, e, o, c, f) {
		return u(r ^ (t | ~e), n, t, o, c, f)
	}
	function a(n, t) {
		n[t >> 5] |= 128 << t % 32, n[(t + 64 >>> 9 << 4) + 14] = t;
		var e, u, a, h, g, d = 1732584193,
			l = -271733879,
			v = -1732584194,
			s = 271733878;
		for (e = 0; e < n.length; e += 16) u = d, a = l, h = v, g = s, d = o(d, l, v, s, n[e], 7, -680876936), s = o(s, d, l, v, n[e + 1], 12, -389564586), v = o(v, s, d, l, n[e + 2], 17, 606105819), l = o(l, v, s, d, n[e + 3], 22, -1044525330), d = o(d, l, v, s, n[e + 4], 7, -176418897), s = o(s, d, l, v, n[e + 5], 12, 1200080426), v = o(v, s, d, l, n[e + 6], 17, -1473231341), l = o(l, v, s, d, n[e + 7], 22, -45705983), d = o(d, l, v, s, n[e + 8], 7, 1770035416), s = o(s, d, l, v, n[e + 9], 12, -1958414417), v = o(v, s, d, l, n[e + 10], 17, -42063), l = o(l, v, s, d, n[e + 11], 22, -1990404162), d = o(d, l, v, s, n[e + 12], 7, 1804603682), s = o(s, d, l, v, n[e + 13], 12, -40341101), v = o(v, s, d, l, n[e + 14], 17, -1502002290), l = o(l, v, s, d, n[e + 15], 22, 1236535329), d = c(d, l, v, s, n[e + 1], 5, -165796510), s = c(s, d, l, v, n[e + 6], 9, -1069501632), v = c(v, s, d, l, n[e + 11], 14, 643717713), l = c(l, v, s, d, n[e], 20, -373897302), d = c(d, l, v, s, n[e + 5], 5, -701558691), s = c(s, d, l, v, n[e + 10], 9, 38016083), v = c(v, s, d, l, n[e + 15], 14, -660478335), l = c(l, v, s, d, n[e + 4], 20, -405537848), d = c(d, l, v, s, n[e + 9], 5, 568446438), s = c(s, d, l, v, n[e + 14], 9, -1019803690), v = c(v, s, d, l, n[e + 3], 14, -187363961), l = c(l, v, s, d, n[e + 8], 20, 1163531501), d = c(d, l, v, s, n[e + 13], 5, -1444681467), s = c(s, d, l, v, n[e + 2], 9, -51403784), v = c(v, s, d, l, n[e + 7], 14, 1735328473), l = c(l, v, s, d, n[e + 12], 20, -1926607734), d = f(d, l, v, s, n[e + 5], 4, -378558), s = f(s, d, l, v, n[e + 8], 11, -2022574463), v = f(v, s, d, l, n[e + 11], 16, 1839030562), l = f(l, v, s, d, n[e + 14], 23, -35309556), d = f(d, l, v, s, n[e + 1], 4, -1530992060), s = f(s, d, l, v, n[e + 4], 11, 1272893353), v = f(v, s, d, l, n[e + 7], 16, -155497632), l = f(l, v, s, d, n[e + 10], 23, -1094730640), d = f(d, l, v, s, n[e + 13], 4, 681279174), s = f(s, d, l, v, n[e], 11, -358537222), v = f(v, s, d, l, n[e + 3], 16, -722521979), l = f(l, v, s, d, n[e + 6], 23, 76029189), d = f(d, l, v, s, n[e + 9], 4, -640364487), s = f(s, d, l, v, n[e + 12], 11, -421815835), v = f(v, s, d, l, n[e + 15], 16, 530742520), l = f(l, v, s, d, n[e + 2], 23, -995338651), d = i(d, l, v, s, n[e], 6, -198630844), s = i(s, d, l, v, n[e + 7], 10, 1126891415), v = i(v, s, d, l, n[e + 14], 15, -1416354905), l = i(l, v, s, d, n[e + 5], 21, -57434055), d = i(d, l, v, s, n[e + 12], 6, 1700485571), s = i(s, d, l, v, n[e + 3], 10, -1894986606), v = i(v, s, d, l, n[e + 10], 15, -1051523), l = i(l, v, s, d, n[e + 1], 21, -2054922799), d = i(d, l, v, s, n[e + 8], 6, 1873313359), s = i(s, d, l, v, n[e + 15], 10, -30611744), v = i(v, s, d, l, n[e + 6], 15, -1560198380), l = i(l, v, s, d, n[e + 13], 21, 1309151649), d = i(d, l, v, s, n[e + 4], 6, -145523070), s = i(s, d, l, v, n[e + 11], 10, -1120210379), v = i(v, s, d, l, n[e + 2], 15, 718787259), l = i(l, v, s, d, n[e + 9], 21, -343485551), d = r(d, u), l = r(l, a), v = r(v, h), s = r(s, g);
		return [d, l, v, s]
	}
	function h(n) {
		var t, r = "";
		for (t = 0; t < 32 * n.length; t += 8) r += String.fromCharCode(n[t >> 5] >>> t % 32 & 255);
		return r
	}
	function g(n) {
		var t, r = [];
		for (r[(n.length >> 2) - 1] = void 0, t = 0; t < r.length; t += 1) r[t] = 0;
		for (t = 0; t < 8 * n.length; t += 8) r[t >> 5] |= (255 & n.charCodeAt(t / 8)) << t % 32;
		return r
	}
	function d(n) {
		return h(a(g(n), 8 * n.length))
	}
	function l(n, t) {
		var r, e, u = g(n),
			o = [],
			c = [];
		for (o[15] = c[15] = void 0, u.length > 16 && (u = a(u, 8 * n.length)), r = 0; 16 > r; r += 1) o[r] = 909522486 ^ u[r], c[r] = 1549556828 ^ u[r];
		return e = a(o.concat(g(t)), 512 + 8 * t.length), h(a(c.concat(e), 640))
	}
	function v(n) {
		var t, r, e = "0123456789abcdef",
			u = "";
		for (r = 0; r < n.length; r += 1) t = n.charCodeAt(r), u += e.charAt(t >>> 4 & 15) + e.charAt(15 & t);
		return u
	}
	function s(n) {
		return unescape(encodeURIComponent(n))
	}
	function C(n) {
		return d(s(n))
	}
	function A(n) {
		return v(C(n))
	}
	'''


str = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":1528628815464,"param":{"user_id":0,"visited_user_id":66546564,"keyword":"","year":0,"length":18,"start":0},"sign_code":"b7df15fc5ccf64e9fa3"}'
jsonObj = json.loads(str)
print(jsonObj['sign_code'])
param = json.dumps(jsonObj['param'])
ctx = execjs.compile(js)
print(ctx.call('A', param)[5,24])



