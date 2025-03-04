Here's the **human-written** README for your **AWS Serverless Job Portal** project:  

---

# **AWS Serverless Job Portal 🚀**  

This is a **serverless job portal** built with AWS services, designed to be scalable and cost-efficient. The portal allows users to **view job listings** and **add new jobs**, using a fully managed backend with **Lambda, API Gateway, and DynamoDB**. The frontend is hosted on **S3**, and **CloudFront** ensures secure HTTPS access.  

## **🛠️ Tech Stack**  
- **S3** → Hosts the frontend (HTML, CSS, JavaScript)  
- **DynamoDB** → Stores job listings  
- **Lambda** → Handles backend logic (GET & POST jobs)  
- **API Gateway (REST API)** → Exposes Lambda functions as HTTP endpoints  
- **CloudFront** → Enables HTTPS and improves performance  

---

## **📌 Features**  
✅ Fetch and display job listings  
✅ Add new job postings dynamically  
✅ HTTPS-secured frontend with CloudFront  
✅ Fully serverless and scalable architecture  

---

## **1️⃣ Setting Up AWS Services**  

### **🖥️ 1.1 Create an S3 Bucket (Frontend Hosting)**  
1. Go to **AWS S3 Console** → Click **Create Bucket**.  
2. **Disable "Block Public Access"** (uncheck all options).  
3. In the **Properties** tab, enable **Static Website Hosting**.  
4. Upload `index.html` and `script.js`.  
5. Note the **S3 website URL** (e.g., `http://your-bucket.s3-website-us-east-1.amazonaws.com`).  

---

### **🛠️ 1.2 Setup DynamoDB (Job Storage)**  
1. Open **AWS DynamoDB Console** → Click **Create Table**.  
2. Table Name: `JobTable`  
3. Primary Key: `jobId` (String)  
4. Click **Create**.  

---

### **📝 1.3 Create Lambda Functions (Backend Logic)**  

#### **📌 1.3.1 Lambda for Fetching Jobs (GET)**  
1. Open **AWS Lambda Console** → Click **Create Function**.  
2. Name: `GetJobsLambda`, Runtime: **Python 3.9**.  
3. Assign **AWSLambdaBasicExecutionRole** & **DynamoDB Read Access**.  
4. Add the following code:  

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

#### **📌 1.3.2 Lambda for Adding Jobs (POST)**  
1. Go to **AWS Lambda Console** → Click **Create Function**.  
2. Name: `PostJobsLambda`, Runtime: **Python 3.9**.  
3. Assign **AWSLambdaBasicExecutionRole** & **DynamoDB Write Access**.  
4. Add the following code:  

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
1. Open **AWS API Gateway Console** → Click **Create REST API**.  
2. **Create a Resource** → `/jobs`.  
3. Add **Methods**:  
   - **GET** → Integrate with `GetJobsLambda`.  
   - **POST** → Integrate with `PostJobsLambda`.  

4. **Enable CORS for `/jobs`**:  
   - Allowed Origins: `*`  
   - Allowed Methods: `GET, POST`  
   - Headers: `Content-Type`  

5. Deploy the API → **Create a new stage (prod)**.  
6. Copy the **API Invoke URL** (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/prod/jobs`).  

---

### **🔒 1.5 Setup CloudFront (HTTPS & CDN)**  
1. Open **AWS CloudFront Console** → Click **Create Distribution**.  
2. **Origin Domain**: Use your **S3 static website URL**.  
3. **Origin Protocol Policy**: Set to **HTTP Only**.  
4. **Viewer Protocol Policy**: Select **Redirect HTTP to HTTPS**.  
5. **Cache Policy**: Use default settings.  
6. **SSL Certificate**: Request a free certificate via **AWS Certificate Manager (ACM)**.  
7. Click **Create** and wait (~10 min) for deployment.  
8. Copy the **CloudFront URL** (e.g., `https://dxyz.cloudfront.net`).  

---

## **2️⃣ Update the Frontend Code**  

Edit `index.html` to use the **CloudFront URL** and **API Gateway URL**:  

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
2. Open your **CloudFront URL** to test the website.  

---

## **3️⃣ Cleaning Up (Avoid Charges)**  
If you **don’t want charges**, delete the following AWS resources:  
✅ **CloudFront Distribution**  
✅ **API Gateway**  
✅ **Lambda Functions**  
✅ **DynamoDB Table**  
✅ **S3 Bucket**  

---
