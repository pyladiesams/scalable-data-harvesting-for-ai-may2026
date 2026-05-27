## Selector quick reference

### Basic selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `*` | Any element | |
| `tag` | Elements by tag name | `p`, `h1`, `a`, `div` |
| `.class` | Elements with a class | `.nav-item`, `.highlight` |
| `#id` | Element with a specific id | `#main`, `#header` |

### Combinators

| Selector | Description | Example |
|----------|-------------|---------|
| `A B` | B anywhere inside A (descendant) | `div p`, `ul li` |
| `A > B` | B as a direct child of A | `ul > li` |
| `A + B` | B immediately after A (adjacent sibling) | `h2 + p` |
| `A ~ B` | All B siblings after A | `h2 ~ p` |

### Attribute selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `[attr]` | Has the attribute | `a[href]`, `input[disabled]` |
| `[attr="val"]` | Exact match | `input[type="submit"]` |
| `[attr*="val"]` | Contains substring | `a[href*="example"]` |
| `[attr^="val"]` | Starts with | `a[href^="https"]` |
| `[attr$="val"]` | Ends with | `a[href$=".pdf"]` |

### Pseudo-classes

| Selector | Description | Example |
|----------|-------------|---------|
| `:first-child` | First child of its parent | |
| `:last-child` | Last child of its parent | |
| `:nth-child(n)` | nth child; use `2n` for even rows | |
| `:not(selector)` | Elements that do not match | `li:not(.active)` |

### Scrapy / parsel pseudo-elements

| Selector | Description | Example |
|----------|-------------|---------|
| `::text` | Direct text content of the element | `h1::text` → `"Hello"` |
| `::attr(name)` | Value of an attribute | `a::attr(href)`, `img::attr(src)` |

### Combining with `.get()` / `.getall()`

| Method | Description |
|--------|-------------|
| `.get()` | First match as a string (or `None`) |
| `.get("fallback")` | First match with a default value |
| `.getall()` | All matches as a list of strings |

### Common patterns

| Selector | Description |
|----------|-------------|
| `a::attr(href)` | All link URLs |
| `img::attr(src)` | Image source paths |
| `.price::text` | Text inside a price element |
| `td:nth-child(2)::text` | Text from the second table column |
| `ul.menu > li > a::attr(href)` | Links in a direct-child nav list |