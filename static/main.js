import filteredJobs from './data.json' with { type: 'json' };
// const filteredJobs = [];

const container = document.getElementById('container');


// function getOffers() {
//   for (let i = 0; i < 8; ++i) {
//     const jobCard = document.createElement('div');
//     jobCard.classList.add('job-card')
//     jobCard.textContent()
//     jobHolder.append(jobCard)
//   }
// }

console.log(filteredJobs.name);
//if the search is not empty create this element
const jobHolder = document.getElementById('job-holder');

// Equivalent to v-if="filteredJobs.length > 0"
if (filteredJobs.length > 0) {
  
  // Equivalent to v-for="job in filteredJobs"
  filteredJobs.forEach(job => {
    
    // 1. Create the main card div
    const jobCard = document.createElement('div');
    jobCard.className = 'job-card';

    // 2. Create the Title (h2)
    const title = document.createElement('h2');
    title.className = 'job-title';
    title.textContent = job.title;

    // 3. Create Company Name
    const company = document.createElement('div');
    company.className = 'company-name';
    company.textContent = job.company;

    // 4. Create Details
    const details = document.createElement('div');
    details.className = 'details';
    details.textContent = `${job.location} • ${job.postedDate}`;

    // 5. Create Stipend (with conditional logic)
    const stipend = document.createElement('div');
    stipend.className = 'stipend';
    stipend.textContent = job.stipend > 0 ? `$${job.stipend}` : 'Unpaid';

    // 6. Create Badge (with dynamic classes)
    const badge = document.createElement('div');
    const isPaid = job.stipend > 0;
    badge.classList.add('badge', isPaid ? 'badge-paid' : 'badge-unpaid');
    badge.textContent = isPaid ? 'Paid' : 'Unpaid';

    // 7. Assemble the card
    jobCard.append(title, company, details, stipend, badge);

    // 8. Add the completed card to the DOM
    jobHolder.append(jobCard);
  });
} else {
  const noResults = document.createElement('div');
  noResults.classList.add('no-results');

  noResults.append( () => {
    document
    .createElement('h3')
    .textContent('No internships found matching your search.')
  }
)
  container.append(noResults)
//   <div v-else class="no-results">
//     <h3>No internships found matching your search.</h3>
//   </div>
}
// <div id="app" class="container">
//   <header>
//     <h1>🎓 GradJobs</h1>
//     <p>The best internships for new graduates, all in one place.</p>
//   </header>
//
//   <div class="toolbar">
//     <input type="text" v-model="searchQuery" placeholder="Search job titles...">
//
//     <label for="sort">Sort by:</label>
//     <select id="sort" v-model="sortKey">
//       <option value="newest">Newest First</option>
//       <option value="money-high">Stipend: High to Low</option>
//       <option value="money-low">Stipend: Low to High</option>
//       <option value="company">Company Name (A-Z)</option>
//     </select>
//   </div>
//
//   <div v-if="filteredJobs.length > 0">
//     <div v-for="job in filteredJobs" :key="job.id" class="job-card">
//       <h2 class="job-title">{{ job.title }}</h2>
//       <div class="company-name">{{ job.company }}</div>
//       <div class="details">{{ job.location }} • {{ job.postedDate }}</div>
//
//       <div class="stipend">
//         Stipend: {{ job.stipend > 0 ? '$' + job.stipend : 'Unpaid' }}
//       </div>
//
//       <div :class="['badge', job.stipend > 0 ? 'badge-paid' : 'badge-unpaid']">
//         {{ job.stipend > 0 ? 'Paid' : 'Unpaid' }}
//       </div>
//     </div>
//   </div>
//
//   <div v-else class="no-results">
//     <h3>No internships found matching your search.</h3>
//   </div>
// </div>
