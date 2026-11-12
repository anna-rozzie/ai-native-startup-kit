// Discovery Log: pure logic, shared by the app and the tests.
(function (root) {
  function cleanTags(text) {
    var seen = {}, out = [];
    String(text || "").split(",").forEach(function (t) {
      var tag = t.trim().toLowerCase().replace(/\s+/g, " ");
      if (tag && !seen[tag]) { seen[tag] = true; out.push(tag); }
    });
    return out;
  }
  function addInterview(list, input) {
    var who = String((input && input.who) || "").trim();
    if (!who) return { ok: false, error: "Who did you talk to?", list: list };
    var item = {
      id: Date.now() + "-" + Math.random().toString(36).slice(2, 7),
      who: who,
      date: (input.date || new Date().toISOString().slice(0, 10)),
      notes: String(input.notes || "").trim(),
      pains: cleanTags(input.pains)
    };
    return { ok: true, list: [item].concat(list), item: item };
  }
  function removeInterview(list, id) {
    return list.filter(function (i) { return i.id !== id; });
  }
  // Each pain counts once per interview, so one talkative person cannot skew it.
  function topPains(list) {
    var counts = {};
    list.forEach(function (i) {
      i.pains.forEach(function (p) { counts[p] = (counts[p] || 0) + 1; });
    });
    return Object.keys(counts).map(function (p) {
      return { pain: p, count: counts[p], share: list.length ? counts[p] / list.length : 0 };
    }).sort(function (a, b) { return b.count - a.count || a.pain.localeCompare(b.pain); });
  }
  function load(storage) {
    try {
      var data = JSON.parse(storage.getItem("discovery-log") || "[]");
      return Array.isArray(data) ? data : [];
    } catch (e) { return []; }
  }
  function save(storage, list) { storage.setItem("discovery-log", JSON.stringify(list)); }
  var api = { cleanTags: cleanTags, addInterview: addInterview, removeInterview: removeInterview, topPains: topPains, load: load, save: save };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.DL = api;
})(this);
