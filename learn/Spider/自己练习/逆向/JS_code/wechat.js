function S(t, i) {
  var n = (t & 65535) + (i & 65535),
    d = (t >> 16) + (i >> 16) + (n >> 16)
  return (d << 16) | (n & 65535)
}
function R(t, i) {
  return (t << i) | (t >>> (32 - i))
}
function y(t, i, n, d, C, E) {
  return S(R(S(S(i, t), S(d, E)), C), n)
}
function b(t, i, n, d, C, E, F) {
  return y((i & n) | (~i & d), t, i, C, E, F)
}
function a(t, i, n, d, C, E, F) {
  return y((i & d) | (n & ~d), t, i, C, E, F)
}
function o(t, i, n, d, C, E, F) {
  return y(i ^ n ^ d, t, i, C, E, F)
}
function p(t, i, n, d, C, E, F) {
  return y(n ^ (i | ~d), t, i, C, E, F)
}
function s(t, i) {
  t[i >> 5] |= 128 << i % 32
  t[(((i + 64) >>> 9) << 4) + 14] = i
  var n,
    d,
    C,
    E,
    F,
    u = 1732584193,
    f = -271733879,
    h = -1732584194,
    r = 271733878
  for (n = 0; n < t.length; n += 16) {
    d = u
    C = f
    E = h
    F = r
    u = b(u, f, h, r, t[n], 7, -680876936)
    r = b(r, u, f, h, t[n + 1], 12, -389564586)
    h = b(h, r, u, f, t[n + 2], 17, 606105819)
    f = b(f, h, r, u, t[n + 3], 22, -1044525330)
    u = b(u, f, h, r, t[n + 4], 7, -176418897)
    r = b(r, u, f, h, t[n + 5], 12, 1200080426)
    h = b(h, r, u, f, t[n + 6], 17, -1473231341)
    f = b(f, h, r, u, t[n + 7], 22, -45705983)
    u = b(u, f, h, r, t[n + 8], 7, 1770035416)
    r = b(r, u, f, h, t[n + 9], 12, -1958414417)
    h = b(h, r, u, f, t[n + 10], 17, -42063)
    f = b(f, h, r, u, t[n + 11], 22, -1990404162)
    u = b(u, f, h, r, t[n + 12], 7, 1804603682)
    r = b(r, u, f, h, t[n + 13], 12, -40341101)
    h = b(h, r, u, f, t[n + 14], 17, -1502002290)
    f = b(f, h, r, u, t[n + 15], 22, 1236535329)
    u = a(u, f, h, r, t[n + 1], 5, -165796510)
    r = a(r, u, f, h, t[n + 6], 9, -1069501632)
    h = a(h, r, u, f, t[n + 11], 14, 643717713)
    f = a(f, h, r, u, t[n], 20, -373897302)
    u = a(u, f, h, r, t[n + 5], 5, -701558691)
    r = a(r, u, f, h, t[n + 10], 9, 38016083)
    h = a(h, r, u, f, t[n + 15], 14, -660478335)
    f = a(f, h, r, u, t[n + 4], 20, -405537848)
    u = a(u, f, h, r, t[n + 9], 5, 568446438)
    r = a(r, u, f, h, t[n + 14], 9, -1019803690)
    h = a(h, r, u, f, t[n + 3], 14, -187363961)
    f = a(f, h, r, u, t[n + 8], 20, 1163531501)
    u = a(u, f, h, r, t[n + 13], 5, -1444681467)
    r = a(r, u, f, h, t[n + 2], 9, -51403784)
    h = a(h, r, u, f, t[n + 7], 14, 1735328473)
    f = a(f, h, r, u, t[n + 12], 20, -1926607734)
    u = o(u, f, h, r, t[n + 5], 4, -378558)
    r = o(r, u, f, h, t[n + 8], 11, -2022574463)
    h = o(h, r, u, f, t[n + 11], 16, 1839030562)
    f = o(f, h, r, u, t[n + 14], 23, -35309556)
    u = o(u, f, h, r, t[n + 1], 4, -1530992060)
    r = o(r, u, f, h, t[n + 4], 11, 1272893353)
    h = o(h, r, u, f, t[n + 7], 16, -155497632)
    f = o(f, h, r, u, t[n + 10], 23, -1094730640)
    u = o(u, f, h, r, t[n + 13], 4, 681279174)
    r = o(r, u, f, h, t[n], 11, -358537222)
    h = o(h, r, u, f, t[n + 3], 16, -722521979)
    f = o(f, h, r, u, t[n + 6], 23, 76029189)
    u = o(u, f, h, r, t[n + 9], 4, -640364487)
    r = o(r, u, f, h, t[n + 12], 11, -421815835)
    h = o(h, r, u, f, t[n + 15], 16, 530742520)
    f = o(f, h, r, u, t[n + 2], 23, -995338651)
    u = p(u, f, h, r, t[n], 6, -198630844)
    r = p(r, u, f, h, t[n + 7], 10, 1126891415)
    h = p(h, r, u, f, t[n + 14], 15, -1416354905)
    f = p(f, h, r, u, t[n + 5], 21, -57434055)
    u = p(u, f, h, r, t[n + 12], 6, 1700485571)
    r = p(r, u, f, h, t[n + 3], 10, -1894986606)
    h = p(h, r, u, f, t[n + 10], 15, -1051523)
    f = p(f, h, r, u, t[n + 1], 21, -2054922799)
    u = p(u, f, h, r, t[n + 8], 6, 1873313359)
    r = p(r, u, f, h, t[n + 15], 10, -30611744)
    h = p(h, r, u, f, t[n + 6], 15, -1560198380)
    f = p(f, h, r, u, t[n + 13], 21, 1309151649)
    u = p(u, f, h, r, t[n + 4], 6, -145523070)
    r = p(r, u, f, h, t[n + 11], 10, -1120210379)
    h = p(h, r, u, f, t[n + 2], 15, 718787259)
    f = p(f, h, r, u, t[n + 9], 21, -343485551)
    u = S(u, d)
    f = S(f, C)
    h = S(h, E)
    r = S(r, F)
  }
  return [u, f, h, r]
}
function l(t) {
  var i,
    n = ''
  for (i = 0; i < t.length * 32; i += 8) {
    n += String.fromCharCode((t[i >> 5] >>> i % 32) & 255)
  }
  return n
}
function w(t) {
  var i,
    n = []
  n[(t.length >> 2) - 1] = void 0
  for (i = 0; i < n.length; i += 1) {
    n[i] = 0
  }
  for (i = 0; i < t.length * 8; i += 8) {
    n[i >> 5] |= (t.charCodeAt(i / 8) & 255) << i % 32
  }
  return n
}
function T(t) {
  return l(s(w(t), t.length * 8))
}
function v(t, i) {
  var n,
    d = w(t),
    C = [],
    E = [],
    F
  C[15] = E[15] = void 0
  if (d.length > 16) {
    d = s(d, t.length * 8)
  }
  for (n = 0; n < 16; n += 1) {
    C[n] = d[n] ^ 909522486
    E[n] = d[n] ^ 1549556828
  }
  F = s(C.concat(w(i)), 512 + i.length * 8)
  return l(s(E.concat(F), 512 + 128))
}
function k(t) {
  var i = '0123456789abcdef',
    n = '',
    d,
    C
  for (C = 0; C < t.length; C += 1) {
    d = t.charCodeAt(C)
    n += i.charAt((d >>> 4) & 15) + i.charAt(d & 15)
  }
  return n
}
function I(t) {
  return unescape(encodeURIComponent(t))
}
function D(t) {
  return T(I(t))
}
function x(t) {
  return k(D(t))
}
function B(t, i) {
  return v(I(t), I(i))
}
function g(t, i) {
  return k(B(t, i))
}
function get_pwd(t, i, n) {
  if (!i) {
    if (!n) {
      return x(t)
    } else {
      return D(t)
    }
  }
  if (!n) {
    return g(i, t)
  } else {
    return B(i, t)
  }
}
