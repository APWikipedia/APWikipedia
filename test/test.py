categories = sorted(list(set(
    [
    "Machine learning", "Deep learning", "Internet search engines", "Data science",
    "Computer Vision","Natural Language Processing","Big Data","Cloud Computing",
    "Internet of Things","Software Engineering","Computer Networks","Cybersecurity",
    "Mobile App Development","Operating Systems","Programming Languages", 
    "Algorithms","Database Technologies","Distributed Systems",
    # # 以上词条能爬取4922篇，耗时一小时
    # # 新增类别，谁来爬一下，挂几小时机

    #  # 每人18行先 雷
    "Artificial Intelligence", "Human-Computer Interaction", "Quantum Computing",
    "Virtual Reality", "Augmented Reality", "Blockchain", "Cryptocurrency",
    "Digital Signal Processing", "Game Development", "Web Development",
    "Computer Graphics", "User Experience Design", "Network Security",
    "Parallel Computing", "Embedded Systems", "Computer Architecture",
    "Information Retrieval", "E-Commerce Technology", "Computational Biology",
    "Computational Physics", "Mathematical Software", "Ethical Hacking",
    "Robotics", "Automation", "Digital Marketing", "Social Media Technology",
    "Cloud Security", "Data Mining", "Machine Ethics", "Bioinformatics",
    "Computer-Aided Design", "Computer Animation", "Wireless Networks",
    "Wearable Technology", "5G Technology", "Edge Computing", "Fintech",
    "Smart Cities", "Digital Art", "Information Theory", "Acoustic Engineering",
    "Software Testing", "DevOps", "Agile Software Development", "System Administration",
    "Data Visualization", "Graph Theory", "Information Systems", "IT Management",
    "Quantum Information Science", "Computational Chemistry", "Digital Humanities",
    "Technology Ethics", "Digital Privacy", "Cyber Physical Systems", "Information Economics",
    "Ubiquitous Computing", "Human-Robot Interaction", "Computational Finance",
    "Digital Forensics", "Autonomous Vehicles", "Cognitive Computing", "Applied Mathematics",
    # 沈
    "Data Ethics", "Sustainable Computing", "Green IT", "Computational Sociology",
    "Technology Management", "Educational Technology", "Health Informatics",
    "Neural Networks", "Evolutionary Computation", "High Performance Computing",
    "Open Source Software", "Software Metrics", "Network Management",
    "Digital Libraries", "Technology Policy", "Digital Accessibility",
    "Computational Geometry", "Pattern Recognition", "Computer Music",
    "Multimedia Systems", "Speech Processing", "Sensor Networks", "Haptic Technology",
    "Real-Time Systems", "Computer Forensics", "IT Legislation", "IT Project Management",
    "Computational Astrophysics", "Cyber Warfare", "Human-Centered Computing",
    "Cryptography", "Data Storage Systems", "Computer Ethics", "Cloud Storage",
    "Enterprise Software", "Graphical User Interfaces", "Digital Signal Processors",
    "Mobile Networking", "Ad Hoc Networks", "Microprocessor Design", "VLSI Design",
    "Wearable Computing", "Computer Simulation", "Digital Signal Controllers",
    "Microcontrollers", "Optical Computing", "Quantum Cryptography",
    "Computer-Aided Engineering", "Computer-Aided Manufacturing", "Virtual Machines",
    "Computer Performance", "Distributed Database", "IT Service Management",
    "Multimedia Networking", "Network Security Algorithms", "Parallel Programming",
    "Programmable Logic", "Reconfigurable Computing", "RFID Technology",
    # # 姜
    "Software Quality Assurance", "Speech Recognition Technology", "System On Chip",
    "Virtual Reality Gaming", "Web Engineering", "Wireless Sensor Networks",
    "Computer Security Incident Management", "Data Privacy Laws", "Edge Computing Architectures",
    "Fuzzy Logic Systems", "Genetic Algorithms", "Hardware Security Modules",
    "Information Theory in Cryptography", "IoT Security Protocols", "Machine Learning in Bioinformatics",
    "Neural Network Optimization", "Quantum Machine Learning", "Reinforcement Learning Applications",
    "Social Network Analysis Algorithms", "Software Defined Networking", "Virtualization Security",
    "Web Scraping Techniques", "3D Computer Graphics", "Advanced Database Systems",
    "Augmented Reality Development", "Biometric Authentication Technologies",
    "Cloud Computing Security", "Computer Animation Techniques", "Data Compression Algorithms",
    "Digital Currency Technologies", "Electronic Voting Systems", "Forensic Data Analysis",
    "GPU Programming", "High-Throughput Computing", "IT Compliance and Ethics",
    "Knowledge Representation and Reasoning", "Low-Power Computing", "Mobile Payment Systems",
    "Network Function Virtualization", "Open Source Intelligence Techniques", "Predictive Analytics Models",
    "Quantum Communication Networks", "Remote Sensing Technology", "Smart Grid Cybersecurity",
    "Text Mining Algorithms", "Ubiquitous Networking", "Virtual Private Networks",
    "Web Accessibility Standards", "Zigbee Communication Protocols", "Adaptive Learning Systems",
    "Biologically Inspired Computing", "Computational Aerodynamics", "Data Fusion Techniques",
    # 唐
    "Embedded Software Development", "Gesture Recognition Systems", "Homomorphic Encryption Methods",
    "Indoor Positioning Systems", "Location-Based Services", "Mobile Device Forensics",
    "Neuromorphic Computing", "Optical Character Recognition", "Program Synthesis",
    "Quantum Information Processing", "Robotics Control Systems", "Space Computing Technology",
    "Threat Intelligence Platforms", "User Interface Design Principles", "Voice Recognition Technologies",
    "Wearable Device Technologies", "3D Printing Technologies", "Automated Reasoning Systems",
    "Blockchain in Healthcare", "Computational Fluid Dynamics", "Data Warehousing Solutions",
    "Enterprise Resource Planning", "Game Theory in Computer Science", "Hybrid Cloud Solutions",
    "Integrated Development Environments", "Log File Analysis Techniques", "Multimedia Learning Systems",
    "Non-Fungible Token Technologies", "Operating System Development", "Privacy Enhancing Technologies",
    "Radio Frequency Identification", "Semantic Web Technologies", "Supply Chain Management Software",
    "Time Series Analysis in Finance", "User Generated Content Moderation", "Virtual Reality in Medicine",
    "Wireless Communication Standards", "Zero Trust Network Architectures",

    "Artificial Intelligence", "Blockchain", "Quantum Computing", "Robotics",
    "Augmented Reality", "Virtual Reality", "Game Development", "Computer Hardware",
    "Human-Computer Interaction", "Information Systems", "Network Security",
    "Graph Theory", "Parallel Computing", "Cryptography", "Data Mining",
    "Embedded Systems", "Computer Graphics", "Web Development", "E-Commerce",
    "Digital Marketing", "Bioinformatics", "Computational Biology", "Cognitive Science",
    "User Experience Design", "Wireless Networks", "Computer Animation", "Digital Art",
    "Educational Technology", "Information Retrieval", "Software Testing",
    "Software Metrics", "Software Modeling", "Agile Software Development",
    "DevOps", "Data Visualization", "User Interface Design", "Systems Engineering",
    "Real-Time Computing", "Digital Signal Processing", "Microprocessors",
    "Quantum Information Science", "Data Structures", "Functional Programming",
    "Object-Oriented Programming", "Logic Programming", "Concurrent Programming",
    "Formal Methods", "Software Architecture", "Network Protocols", "Web Services",
    "Cloud Security", "Machine Ethics", "Computational Linguistics", "Semantic Web",
    "Digital Libraries", "Computer Aided Design", "IT Project Management",
    "Network Management", "Systems Analysis", "Data Quality", "Computational Chemistry",
    "Computational Physics", "Computer-Aided Engineering", "Knowledge Management",
    "Social Network Analysis", "Mobile Computing", "Wearable Technology",
    "Internet Governance", "Digital Privacy", "Cyber Warfare", "Information Ethics",
    "Technology Management", "Information Theory", "Digital Currency", "FinTech",
    "Health Informatics", "Geographic Information Systems", "Urban Informatics",
    "Smart Cities", "Renewable Energy Technology", "Green IT", "Human-Robot Interaction",
    "Autonomous Vehicles", "Quantum Cryptography", "Cloud Storage", "Edge Computing",
    "Internet Protocol", "Software Licensing", "Open Source Software",
    "Computer Forensics", "Data Recovery", "Computer Viruses", "Hacking",
    "Digital Rights Management", "Information Assurance", "IT Governance",
    "Enterprise Architecture", "Business Intelligence", "Customer Relationship Management",
    "Supply Chain Management", "ERP Systems", "Decision Support Systems",
    "E-Government", "Digital Transformation", "Technology Adoption",
    "Innovation Management", "Technology Forecasting", "Computational Neuroscience",
    "Computational Social Science", "Digital Humanities", "Media Technology",
    "Audio Engineering", "Video Game Design", "Esports", "3D Printing",
    "Internet Safety", "Technology Education", "Technology Policy", "Ethical Hacking",
    "Penetration Testing", "Digital Forensics", "Information Security Management",
    "Risk Management", "IT Compliance", "Network Architecture", "Wireless Security",
    "Malware Analysis", "Computer Performance", "Systems Integration",
    "Human Factors Engineering", "Quality Assurance", "IT Service Management",
    "Change Management", "Technical Support", "IT Outsourcing", "Cloud Analytics",
    "Data Center Management", "Virtualization Technology", "Storage Area Networks",
    "Disaster Recovery", "Business Continuity Planning", "IT Auditing", "Cyber Risk Management",
    "Cyber Physical Systems", "Internet Law", "Digital Policy", "Telecommunications Law",
    "Automation","Biotechnology","Cartography","Chemical engineering","Communication ","Media studies","Telecommunications","Construction",
    "Control theory","Design","Digital divide","Earthquake engineering","Energy","Ergonomics","Firefighting","Fire prevention","Forensic science","Forestry","Industry","Information science","Internet","Management","Manufacturing","Marketing","Medicine","Unsolved problems in neuroscience","Metalworking","Microtechnology","Military science","Mining","Nanotechnology","Nuclear technology","Optics","Plumbing","Robotics","Sound technology","Technology forecasting","Tools",
    "Computing","Apps","Artificial intelligence","Classes of computers","Companies","Computer architecture","Computer model","Computer engineering","Computer science","Computer security",
    "Computing and society","Data","Embedded systems","Free software","Human-computer interaction","Information systems","Information technology","Internet","Mobile web","Languages","Multimedia","Networks (Industrial)","Operating systems","Platforms","Product lifecycle management","Programming","Real-time computing","Software","Software engineering","Unsolved problems in computer science",
    "Electronics","Avionics","Circuits","Companies","Connectors","Consumer electronics","Digital electronics","Digital media","Electrical components","Electronic design","Electronics manufacturing","Embedded systems","Integrated circuits","Microwave technology","Molecular electronics","Water technology","Optoelectronics","Quantum electronics","Radio-frequency identification RFID","Radio electronics","Semiconductors","Signal cables","Surveillance","Telecommunications",
    "Electrical engineering","Environmental engineering","Materials science","Mechanical engineering","Nuclear technology","Software engineering","Structural engineering","Systems engineering"
    ]
)))
#print(categories)

def preview_file(file_path, num_lines=10):
    with open(file_path, 'r', encoding='utf-8') as file:
        for _ in range(num_lines):
            print(file.readline().strip())

preview_file('engine/inverted_index.json', 100)  # 查看前5行
