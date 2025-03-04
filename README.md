# **AWS Serverless Job Portal 🚀**  

This is a **serverless job portal** built using AWS services:  
- **S3** → Hosts the frontend (HTML, CSS, JavaScript).  
- **DynamoDB** → Stores job listings.  
- **Lambda** → Handles API logic (GET & POST jobs).  
- **API Gateway (REST API)** → Exposes Lambda functions via HTTP endpoints.  
- **CloudFront** → Provides HTTPS and improves performance.  

---

## **📌 Features**  
✅ List available jobs.  
✅ Add new job listings.  
✅ Secure HTTPS access via CloudFront.  
✅ Fully serverless, scalable, and cost-effective.  

---

## **1️⃣ Setup AWS Services**  

### **🖥️ 1.1 Create an S3 Bucket for Static Website Hosting**  
1. Go to **AWS S3 Console** → **Create bucket**.  
2. **Disable Block Public Access** (uncheck all options).  
3. **Enable Static Website Hosting** under the **Properties** tab.  
4. Upload `index.html`, `script.js`, and other frontend files.  
5. Note the **S3 website endpoint URL** (e.g., `http://your-bucket.s3-website-us-east-1.amazonaws.com`).  

---

### **🛠️ 1.2 Setup DynamoDB (Job Storage)**  
1. Go to **AWS DynamoDB Console** → **Create table**.  
2. Table name: `JobTable`  
3. Primary key: `jobId` (String).  
4. Click **Create**.  

---

### **📝 1.3 Create Lambda Functions (Backend Logic)**  

#### **📌 1.3.1 Create Lambda for Fetching Jobs (GET)**  
1. Go to **AWS Lambda Console** → **Create Function**.  
2. Runtime: **Python 3.9**.  
3. Name: `GetJobsLambda`.  
4. Assign an **IAM role** with **DynamoDB read access**.  
5. Add this code:  

```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobTable')

def lambda_handler(event, context):
    response = table.scan()
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response['Items'])
    }
```

---

#### **📌 1.3.2 Create Lambda for Adding Jobs (POST)**  
1. Go to **AWS Lambda Console** → **Create Function**.  
2. Runtime: **Python 3.9**.  
3. Name: `PostJobsLambda`.  
4. Assign an **IAM role** with **DynamoDB full access**.  
5. Add this code:  

```python
import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobTable')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    job = {
        'jobId': str(uuid.uuid4()),
        'title': data['title'],
        'description': data['description'],
        'company': data['company']
    }
    table.put_item(Item=job)
    return {
        'statusCode': 201,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({"message": "Job added successfully"})
    }
```

---

### **🌐 1.4 Setup API Gateway (REST API)**  
1. Go to **AWS API Gateway Console** → **Create REST API**.  
2. **Create Resource** → `/jobs`.  
3. Add **Methods**:  
   - **GET** → Lambda Integration (`GetJobsLambda`).  
   - **POST** → Lambda Integration (`PostJobsLambda`).  
4. Enable **CORS** for `/jobs`:  
   - Allowed Origins: `*`.  
   - Allowed Methods: `GET, POST`.  
   - Headers: `Content-Type`.  
5. Deploy API → Create a new **Stage (prod)**.  
6. Copy the API **Invoke URL** (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/prod/jobs`).  

---

### **🔒 1.5 Setup CloudFront (HTTPS & CDN)**  
1. Go to **AWS CloudFront Console** → **Create Distribution**.  
2. **Origin Domain**: Use your S3 static website URL.  
3. **Origin Protocol Policy**: HTTP Only.  
4. **Viewer Protocol Policy**: Redirect HTTP to HTTPS.  
5. **Cache Policy**: Use default caching.  
6. **SSL Certificate**: Use AWS Certificate Manager (ACM) to request a free certificate.  
7. Click **Create** and wait (~10 min) for deployment.  
8. Note down the **CloudFront URL** (e.g., `https://dxyz.cloudfront.net`).  

---

## **2️⃣ Update Frontend Code**  
Edit `index.html` to use the **CloudFront URL** and **API Gateway Endpoint**:  

```html
<script>
    const apiUrl = "https://xyz.execute-api.us-east-1.amazonaws.com/prod/jobs";

    async function fetchJobs() {
        try {
            const response = await fetch(apiUrl);
            const jobs = await response.json();
            console.log("Jobs fetched:", jobs);
        } catch (error) {
            console.error("Error:", error);
        }
    }
</script>
```

1. Upload `index.html` to **S3**.  
2. Open the **CloudFront URL** in your browser.  

---

## **3️⃣ Clean-Up (Avoid Charges)**  
If you **don’t want charges**, delete unused AWS resources:  
✅ **S3 Bucket** (if not needed).  
✅ **DynamoDB Table** (if no longer used).  
✅ **Lambda Functions** (`GetJobsLambda`, `PostJobsLambda`).  
✅ **API Gateway** (delete the API).  
✅ **CloudFront Distribution** (if HTTPS is no longer required).  

---
