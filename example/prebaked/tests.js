// Test cases, written before the app. Runs in the browser (tests.html) or with: node tests.js
(function (root) {
  var DL = typeof require !== "undefined" ? require("./logic.js") : root.DL;
  var results = [];
  function test(name, fn) {
    try { fn(); results.push({ name: name, ok: true }); }
    catch (e) { results.push({ name: name, ok: false, error: e.message }); }
  }
  function eq(a, b) {
    if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error("got " + JSON.stringify(a) + ", wanted " + JSON.stringify(b));
  }
  function fakeStorage() { var d = {}; return { getItem: function (k) { return k in d ? d[k] : null; }, setItem: function (k, v) { d[k] = String(v); } }; }

  test("adds an interview to the top of the list", function () {
    var r = DL.addInterview([{ id: "a", who: "Old", pains: [] }], { who: "Sam", pains: "pricing" });
    eq(r.ok, true); eq(r.list.length, 2); eq(r.list[0].who, "Sam");
  });
  test("refuses an interview with no name", function () {
    var r = DL.addInterview([], { who: "   ", pains: "pricing" });
    eq(r.ok, false); eq(r.list.length, 0);
  });
  test("tags are trimmed, lowercased, and deduplicated", function () {
    eq(DL.cleanTags(" Pricing, pricing ,  Slow  Onboarding ,,"), ["pricing", "slow onboarding"]);
  });
  test("empty tag text gives no tags", function () { eq(DL.cleanTags(""), []); eq(DL.cleanTags(null), []); });
  test("top pains are sorted by how many interviews mention them", function () {
    var list = [{ pains: ["pricing", "setup"] }, { pains: ["pricing"] }, { pains: ["setup", "pricing"] }];
    var top = DL.topPains(list);
    eq(top[0].pain, "pricing"); eq(top[0].count, 3); eq(top[1].count, 2);
  });
  test("a pain repeated in one interview counts once", function () {
    var r = DL.addInterview([], { who: "Sam", pains: "pricing, Pricing, pricing" });
    eq(DL.topPains(r.list)[0].count, 1);
  });
  test("ties are broken alphabetically so the order is stable", function () {
    eq(DL.topPains([{ pains: ["zeta", "alpha"] }]).map(function (p) { return p.pain; }), ["alpha", "zeta"]);
  });
  test("no interviews gives no pains", function () { eq(DL.topPains([]), []); });
  test("share is the fraction of interviews that mention the pain", function () {
    eq(DL.topPains([{ pains: ["pricing"] }, { pains: [] }])[0].share, 0.5);
  });
  test("removing an interview removes only that one", function () {
    eq(DL.removeInterview([{ id: "a" }, { id: "b" }], "a"), [{ id: "b" }]);
  });
  test("data survives a save and a reload", function () {
    var s = fakeStorage(); DL.save(s, [{ id: "a", who: "Sam", pains: ["pricing"] }]);
    eq(DL.load(s)[0].who, "Sam");
  });
  test("corrupted saved data loads as an empty list instead of crashing", function () {
    var s = fakeStorage(); s.setItem("discovery-log", "{not json");
    eq(DL.load(s), []);
    s.setItem("discovery-log", '{"a":1}'); eq(DL.load(s), []);
  });

  var failed = results.filter(function (r) { return !r.ok; });
  if (typeof document !== "undefined") {
    document.getElementById("summary").textContent = (results.length - failed.length) + " of " + results.length + " passing";
    document.getElementById("summary").className = failed.length ? "bad" : "good";
    document.getElementById("list").innerHTML = results.map(function (r) {
      return '<li class="' + (r.ok ? "good" : "bad") + '">' + (r.ok ? "PASS" : "FAIL") + "  " + r.name + (r.ok ? "" : " (" + r.error + ")") + "</li>";
    }).join("");
  } else {
    results.forEach(function (r) { console.log((r.ok ? "PASS  " : "FAIL  ") + r.name + (r.ok ? "" : "  " + r.error)); });
    console.log((results.length - failed.length) + " of " + results.length + " passing");
    if (failed.length) process.exit(1);
  }
})(this);
