navbar = """
<nav class="navbar">
  <div class="nav-left">
    <a href="/"><img style="width: 80px; height: 60px" src="image/logo.png"/></a>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li class="dropdown">
        <a href="#">Data Explorer ▾</a>
        <ul class="dropdown-menu">
          <li><a class="inside-link" href="/vaccination">Vaccination</a></li>
          <li><a class="inside-link" href="/Infection">Infection</a></li>
        </ul>
      </li>
      <li class="dropdown">
        <a href="#">Insights ▾</a>
        <ul class="dropdown-menu">
          <li><a class="inside-link" href="/vaccination_insight">Vaccination</a></li>
          <li><a class="inside-link" href="/Infection_Insight">Infection</a></li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="nav-right">
  </div>
</nav>

<script>
  (function() {
    var currentPath = window.location.pathname.toLowerCase();
    var links = document.querySelectorAll(".nav-links a");

    links.forEach(function(link) {
      var href = link.getAttribute("href").toLowerCase();
      var isInsideLink = link.classList.contains("inside-link");

      // only activate if not inside-link
      if (!isInsideLink && href === currentPath) {
        link.classList.add("active");
      }

      // if an inside-link matches current path, highlight parent dropdown only
      if (isInsideLink && href === currentPath) {
        var dropdown = link.closest(".dropdown");
        if (dropdown) {
          var parentLink = dropdown.querySelector("a:not(.inside-link)");
          if (parentLink) parentLink.classList.add("active");
          dropdown.classList.add("open");
        }
      }
    });
  })();
</script>
"""