# Example: LOW VIABILITY Idea

This is a reference example showing what a weak, non-viable idea assessment looks like and how to deliver the bad news compassionately but honestly.

---

# 🔍 Idea Assessment: AI-Powered Recipe Recommendation App

## 🎯 Executive Summary

**Verdict:** TRASH IT 🗑️
**Viability Score:** 28/100 (LOW)
**Confidence Level:** High (80%)

**One-Line Assessment:**
Entering an extremely saturated market with no meaningful differentiation, weak monetization model, and little evidence that customers need yet another recipe app—high probability of failure even with perfect execution.

---

## 📊 Market Analysis

### Market Size & Opportunity
- **TAM:** $800M (recipe and meal planning app market)
- **Growth Rate:** 3% annually (declining from 12% in 2020-2022)
- **Market Stage:** Mature/Declining
- **Score:** 6/20

**Key Findings:**
While the recipe app market is large, it's mature and declining. Growth spike during COVID (2020-2022) has reversed. Market dominated by established free apps (Allrecipes, Tasty) and premium players (Paprika, Mealime). New entrants struggle to gain traction due to network effects and high content expectations.

**Sources:**
- Sensor Tower: Recipe app installs down 18% YoY (2024-2025)
- App Annie: Top 20 recipe apps account for 85% of market share
- Statista: Meal planning app market growth slowing (3.2% projected 2026-2030 vs 12% in 2020-2022)

### Target Customer
- **Primary Persona:** Home cooks looking for recipe inspiration and meal planning
- **Pain Point:** Finding recipes that match ingredients on hand, meal planning for the week
- **Current Solution:** Pinterest, Google Search, YouTube, free apps (Allrecipes, Tasty), cookbooks
- **Willingness to Pay:** Very low—market conditioned to expect free apps with ads

---

## 🥊 Competitive Landscape

### Direct Competitors

| Company | Traction | Differentiation | Threat Level |
|---------|----------|-----------------|--------------|
| Allrecipes | 60M+ users, free | Massive recipe database, community reviews | HIGH |
| Tasty (BuzzFeed) | 40M+ users, free | Video recipes, strong brand, content engine | HIGH |
| Paprika | 1M+ downloads | Paid app ($5), grocery lists, meal planning | MEDIUM |
| Mealime | 5M+ users | Free meal planning, subscription for premium | MEDIUM |
| Yummly | 25M+ users | Personalized recommendations, shopping list | HIGH |
| Whisk | Samsung-backed | Shopping integration, smart kitchen devices | MEDIUM |
| SideChef | 10M+ downloads | Step-by-step voice guidance | MEDIUM |

### Indirect Competitors
- **Google/Pinterest:** Where most people start their recipe search; SEO makes this dominant
- **YouTube:** Video recipes (Binging with Babish, Tasty); huge content advantage
- **Instagram/TikTok:** Food influencers, recipe inspiration; viral distribution
- **Cookbooks:** Still $1B+ market; people like physical books
- **Meal kit services:** HelloFresh, Blue Apron; solve the same problem (what to cook)

### Your Competitive Advantage
**Score:** 4/20

✅ **Claimed Strengths:**
- "AI-powered recommendations" - But Yummly, Mealime already have this
- "Better UX" - Subjective; established apps have years of UX refinement

⚠️ **Reality:**
- No meaningful differentiation from 50+ existing recipe apps
- AI recommendation is table stakes now, not a differentiator
- No unique content, no proprietary recipes, no community
- Can't compete with Tasty's brand or Allrecipes' 10M+ recipe database
- No distribution advantage (they have millions of users already)
- No moat whatsoever—easily copied, already commoditized

---

## 🎯 Customer Validation

**Score:** 5/20

**Evidence of Demand:**
- ❌ **Reddit r/Cooking (3M members):** People asking for recipe sources, but almost always recommending *existing* apps (Paprika, Mealime) or free sources (YouTube, blogs)
- ❌ **r/MealPrepSunday:** Users asking for meal planning tools, but top recommendations are established apps or spreadsheets
- ⚠️ **X/Twitter:** Food bloggers discussing recipe organization, but no unmet needs identified

**Customer Feedback Signals:**

**Reddit:**
- r/Cooking: "What recipe app do you use?" threads show satisfaction with current options
- Top recommendations: Paprika (for paid), Mealime (for free meal planning), Google/Pinterest (for search)
- No complaints about "I wish there was a better recipe app"
- Common sentiment: "I just use Google" or "Pinterest is fine"

**X/Twitter:**
- Food bloggers discuss existing tools they use (Paprika is most loved)
- No trending discussions about needing better recipe apps
- When AI is mentioned, it's mostly skepticism: "I don't want AI telling me what to cook"

**LinkedIn:**
- Professional food industry discussions don't mention consumer recipe apps as a gap
- More focus on B2B opportunities (restaurant tech, supply chain)

**Other:**
- **Product Hunt:** New recipe apps launch regularly but rarely get >200 upvotes or sustained traction
- **App Store reviews:** Existing apps have 4+ star ratings with millions of reviews—users are generally satisfied
- **Google Trends:** "Recipe app" searches declining since 2021 COVID peak

---

## 🛠️ Execution Assessment

**Score:** 9/20

**Can You Build This in <2 Weeks?**
NO - A competitive recipe app requires much more than 2 weeks

**Technical Requirements:**
- **Core tech stack:** React Native (iOS + Android), Node backend, PostgreSQL, Elasticsearch (recipe search)
- **Critical integrations:**
  - Recipe API or database (need 10k+ recipes minimum to compete)
  - AI/ML recommendation engine (OpenAI API or custom model)
  - Nutrition API (MyFitnessPal, Nutritionix)
  - Image storage and optimization (CDN)
- **Complexity rating:** 7/10 - Mobile app development, search functionality, recommendation algorithms, content management

**Why it's complex:**
- Need iOS + Android apps (web alone won't cut it for recipe apps)
- Recipe database: either scrape (legal issues) or build/license (expensive, time-consuming)
- Search functionality needs to be excellent (Elasticsearch or Algolia required)
- Image-heavy app needs CDN and optimization
- Recommendation engine requires ML infrastructure or expensive API calls
- App store approval, updates, platform-specific bugs

**Key Execution Risks:**
1. **Recipe content sourcing** - Mitigation: None that's legal and fast. Licensing is expensive, building takes years, scraping is illegal
2. **Mobile development complexity** - Mitigation: Use React Native, but still requires 4-8 weeks minimum for decent MVP
3. **Search quality expectations** - Mitigation: Users expect Google-level search; Elasticsearch is complex and expensive to run

---

## 💰 Revenue Potential

**Score:** 4/20

**Realistic Year 1 Projections:**
- **Conservative MRR:** $150 (50 users × $2.99/month)
- **Realistic MRR:** $600 (200 users × $2.99/month)
- **Optimistic MRR:** $1,500 (500 users × $2.99/month)

**Why so low?**
- Market expects FREE (Allrecipes, Tasty, Yummly are free with ads)
- Premium apps (Paprika) are one-time $5 purchase, not subscription
- Very hard to acquire users organically (SEO dominated by established players)
- High CAC ($5-20) via paid ads competing with well-funded companies

**Pricing Strategy:**
- **Market expectation:** Free with ads OR $3-5 one-time purchase
- **Subscription fatigue:** Users tired of subscriptions for everything
- **Competitor pricing:**
  - Allrecipes, Tasty, Yummly: Free with ads
  - Paprika: $4.99 one-time
  - Mealime Premium: $6.99/month (but free tier is generous)
  - Market won't support $9.99/month for recipe app
- **Our pricing dilemma:**
  - Free with ads: Need millions of users to generate meaningful revenue (not achievable)
  - $2.99/month subscription: Users ask "why not just use free Allrecipes?"
  - $4.99 one-time: Possibly, but limits LTV to $5 per user

**Unit Economics:**
- **Estimated CAC:** $10-20 (paid ads in crowded market, no organic discovery)
- **LTV (subscription):** $2.99/month × 6 months avg = $18
- **LTV (one-time):** $4.99
- **LTV/CAC ratio:** 0.9x (BROKEN—you lose money on every customer!)

**Key Assumptions:**
1. Can somehow acquire users at $10-20 each (optimistic—likely higher)
2. Users will pay for subscription when free alternatives exist (unlikely)
3. Can retain users for 6 months (optimistic—many will churn after 1-2 months)

---

## 🔥 The Brutally Honest Section

### What's Actually Strong

1. **Large market exists:** There are millions of people who use recipe apps, so the customer base is real.

2. **You could technically build something:** The tech stack is doable (though 4-8 weeks, not 2).

That's... about it. There's not much else strong about this idea.

### Why This Will Almost Certainly Fail

1. **Extremely saturated market:** There are 50+ recipe apps with millions of users. Allrecipes has 60M users. Tasty has BuzzFeed's content engine and brand. You have zero users, zero brand, zero content. Why would anyone switch to your app?

2. **No differentiation:** "AI-powered recommendations" is not differentiation—Yummly has had this for years, Mealime has it, even free apps are adding AI now. What makes you different? "Better UX" is what every app claims, and it's subjective and easily copied.

3. **Broken economics:** If you charge for your app, no one will download it (they'll use free Allrecipes). If you make it free with ads, you need millions of users to make meaningful revenue. You can't acquire millions of users without millions in marketing budget (which you don't have). CAC > LTV = you lose money on every customer.

4. **Distribution is impossible:** How will anyone find your app? SEO is dominated by Allrecipes, Tasty, food blogs. App Store search is dominated by established apps with millions of reviews. Paid ads are expensive ($5-20 CPI) and dominated by funded competitors. You have no distribution channel.

5. **Content is king, and you have none:** Recipe apps are valued for their content. Allrecipes has 10M+ recipes with user ratings. Tasty has professional video content. What do you have? Either you build content (years of work), license it (expensive), or scrape it (illegal). None of these are viable for a bootstrapper.

### Critical Questions You MUST Answer

- [ ] What is your SPECIFIC differentiation that would make someone abandon Allrecipes (free, 60M users, 10M recipes) for your app?
- [ ] How will you acquire your first 1,000 users when SEO is dominated and paid ads are expensive?
- [ ] How will you monetize when users expect free and won't pay for recipe apps?

### The Real Talk

I searched extensively for evidence that people need another recipe app. I found none. Zero.

Instead, I found:
- Threads where people recommend existing apps they're happy with
- Declining interest in recipe apps post-COVID
- Market dominated by free apps with millions of users
- Dozens of failed recipe apps on Product Hunt with <100 users

This market is saturated, commoditized, and dominated by well-funded players or free alternatives. You'd be entering a race you've already lost.

**Would I build this?** Absolutely not. This is a waste of time even if you could build it in 2 weeks (which you can't).

**Would I personally use this?** No. I use Google or YouTube for recipes. If I wanted an app, I'd download Paprika (one-time $5) or use free Allrecipes. Why would I download app #51?

**What about the AI angle?** AI recommendations are table stakes now, not differentiation. Yummly has had AI recommendations since 2014. Every app is adding AI. Users don't care about AI—they care about good recipes and convenience. Your AI doesn't make you special.

The brutal truth: This idea has a <5% chance of reaching $1k MRR even with perfect execution. Your time is worth more than this.

---

## 🎬 Final Recommendation

### TRASH IT 🗑️

**Why Not to Build This:**
- **Extremely saturated market:** 50+ competitors, dominated by free apps with millions of users (Allrecipes, Tasty, Yummly)
- **No meaningful differentiation:** "AI recommendations" is commoditized; every app has this now
- **Broken economics:** CAC ($10-20) > LTV ($18 subscription or $5 one-time) = lose money on every customer
- **Impossible distribution:** Can't compete on SEO (dominated), can't afford paid ads (expensive), no viral mechanism
- **Content problem:** Need thousands of recipes to compete; can't build, license, or scrape legally and cheaply
- **Market expectations:** Users expect free; won't pay for yet another recipe app

**Better Alternatives:**

Instead of building another recipe app, consider these pivots that address the same "helping people cook" space but with less competition:

1. **B2B Food Tech:**
   - Software for restaurant kitchens (inventory, ordering, staff scheduling)
   - Supply chain tech for food distributors
   - Point-of-sale systems for food trucks

2. **Specialized Cooking Niches:**
   - Meal planning specifically for people with dietary restrictions (Celiac, Crohn's, FODMAP)
   - Recipe tools for professional chefs or cooking instructors
   - Ingredient substitution tool for people with allergies

3. **Creator Tools for Food Space:**
   - Tools for food bloggers to monetize (not serving end consumers)
   - Recipe video editing tools
   - Food photography AI tools

**Key Learning:**
When a market has 50+ competitors and is dominated by free offerings with millions of users, you need exceptional differentiation or unfair advantage to succeed. "Better UX" or "AI" is not enough. Sometimes the right move is to not enter the market at all.

---

## 📋 Next Steps

### Time saved: 4-8 weeks of development + 3-6 months of failed marketing attempts

### Better idea directions:

1. **Research underserved cooking niches:**
   - Talk to people with Celiac disease about meal planning challenges
   - Interview professional chefs about software gaps
   - Explore B2B opportunities in restaurant/food service industry

2. **Explore adjacent opportunities:**
   - Kitchen inventory management (track what's in your pantry)
   - Grocery price comparison and optimization
   - Community-based meal swapping (neighbors cook for each other)

3. **Learn from this analysis:**
   - Always check market saturation before building consumer apps
   - Free incumbents with millions of users are nearly impossible to compete with
   - Distribution is harder than building—focus on ideas where you have a distribution advantage
   - "Better" is not differentiation—"Different" is differentiation

---

## 📚 Research Sources

- Sensor Tower: Mobile app download data for recipe category (2024-2025)
- App Annie: Market share analysis for food & drink apps
- Statista: Meal planning app market research (2026-2030 projections)
- Reddit r/Cooking: Searched "recipe app" across 50+ threads (3M members)
- Reddit r/MealPrepSunday: Meal planning tool discussions (2M members)
- X/Twitter: Searched "recipe app recommendations" (100+ tweets analyzed)
- Product Hunt: 30+ recipe app launches reviewed (2023-2025)
- App Store: Top 50 recipe apps reviewed (ratings, reviews, features)
- Google Play Store: Recipe app category analysis
- Google Trends: "Recipe app" search interest (2020-2026)
- Competitor websites: Allrecipes, Tasty, Paprika, Yummly, Mealime, SideChef pricing and features
- Food blogger community discussions (multiple sources)

**Research completed:** February 7, 2026
**Analysis valid through:** May 7, 2026

---

## Why This is a LOW VIABILITY Example

This idea scores 28/100 because:

1. **Market (6/20):** Large but mature/declining, dominated by free players, high market concentration
2. **Competition (4/20):** 50+ competitors, no differentiation, impossible to compete with free incumbents
3. **Demand (5/20):** People use recipe apps, but no evidence of unmet needs—satisfied with current options
4. **Feasibility (9/20):** Could be built but takes 4-8 weeks minimum, complex mobile development + content
5. **Revenue (4/20):** Broken unit economics (CAC > LTV), market expects free, subscription fatigue

**Key Failure Factors:**
- Market saturation (50+ competitors)
- No differentiation (AI is commoditized)
- Broken economics (CAC > LTV)
- No distribution channel (SEO/ads dominated)
- Wrong business model (B2C when should be B2B or niche)

**What Makes This Analysis Good:**
- Brutally honest without being cruel
- Specific evidence of saturation (named competitors, user counts, reviews)
- Explained *why* it will fail (not just "bad idea")
- Provided better alternatives (pivots, related opportunities)
- Showed broken unit economics with real numbers
- Acknowledged what's right (large market exists) while explaining why it doesn't matter
- Framed as "time saved" not "your idea sucks"

**How the Bad News Was Delivered:**
1. Led with data, not opinion
2. Acknowledged what's legitimate about the idea (market exists, buildable)
3. Systematically showed why each dimension fails
4. Used specific evidence (50+ competitors, 60M Allrecipes users, CAC > LTV)
5. Explained rather than dismissed
6. Offered constructive alternatives
7. Positioned as "I'm saving you time and pain" not "you had a bad idea"
