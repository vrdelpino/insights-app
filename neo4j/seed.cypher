// Authors
CREATE (alice:Author {name: "Alice Smith", email: "alice@example.com"});
CREATE (bob:Author {name: "Bob Johnson", email: "bob@example.com"});
CREATE (carol:Author {name: "Carol White", email: "carol@example.com"});
CREATE (alice)-[:MANAGES]->(bob);
CREATE (alice)-[:MANAGES]->(carol);

// Domains
CREATE (finance:Domain {name: "Finance"});
CREATE (marketing:Domain {name: "Marketing"});

// Metrics
CREATE (revenue:Metric {name: "Revenue", definition: "Total income", source: "ERP"});
CREATE (clicks:Metric {name: "Clicks", definition: "Website clicks", source: "Web Logs"});
CREATE (leads:Metric {name: "Leads Generated", definition: "Marketing qualified leads", source: "CRM"});

// Dashboards
CREATE (dashboard1:Dashboard {name: "Executive Overview"});
CREATE (dashboard2:Dashboard {name: "Marketing Funnel"});
CREATE (dashboard3:Dashboard {name: "Financial Summary"});

// Links
CREATE (dashboard1)-[:SHOWS]->(revenue);
CREATE (dashboard1)-[:SHOWS]->(clicks);
CREATE (dashboard2)-[:SHOWS]->(clicks);
CREATE (dashboard2)-[:SHOWS]->(leads);
CREATE (dashboard3)-[:SHOWS]->(revenue);
CREATE (bob)-[:OWNS]->(dashboard1);
CREATE (carol)-[:OWNS]->(dashboard2);
CREATE (alice)-[:OWNS]->(dashboard3);
CREATE (dashboard1)-[:PART_OF]->(finance);
CREATE (dashboard2)-[:PART_OF]->(marketing);
CREATE (dashboard3)-[:PART_OF]->(finance);
