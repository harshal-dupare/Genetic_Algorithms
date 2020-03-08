#include <iostream>
using namespace std;

// function to find root of
float f(float x)
{
    float y = x*x+2*x-13;
    return y;
}

float fit(float x)
{
    float y=f(x);
    return y*y;
}

void merge(float* a,float* b,int p,int q,int l,int k)
{
    int n=q-p+1+k-l+1;
    int m=n-1,i;
    float* c=(float* )malloc(n*sizeof(float));
    float* d=(float* )malloc(n*sizeof(float));
    
    
    while((k>=l)&&(q>=p))
    {
        if(b[k]>=b[q])
        {
            c[m]=a[k];
            d[m]=b[k];
            m--;
            k--;
        }
        else
        {
            c[m]=a[q];
            d[m]=b[q];
            m--;
            q--;
        }
        
    }
    
    while(k>=l)
    {
        c[m]=a[k];
        d[m]=b[k];
        m--;
        k--;
    }
    
    while(q>=p)
    {
        c[m]=a[q];
        d[m]=b[q];
        m--;
        q--;
    }
    
    for(i=0;i<n;i++)
    {
        a[i+p]=c[i];
        b[i+p]=d[i];
    }
    
    return;
}

void mergesort(float* a,float* b,int p,int q)
{
    if(q>p)
    {
        int r=(p+q)/2;
        mergesort(a,b,p,r);
        mergesort(a,b,r+1,q);
        merge(a,b,p,r,r+1,q);
    }
    
    return;
}

void sort(float* a,float* b,int p,int q)
{
    int i=p,j=q,idx;
    float t;
    
    for(j=q;j>0;j--)
    {
        idx=p;
        for(i=p+1;i<=j;i++)
        {
            if(b[i]>b[idx])idx=i;
        }
        t=a[j];
        a[j]=a[idx];
        a[idx]=t;
        t=b[j];
        b[j]=b[idx];
        b[idx]=t;
        
    }
    
    return;
}

void crossover(float* ppl,int n,float x_l,float x_u,float delta,float c_rate)
{
    float c;
    int k,rn1,rn2,i;
    k=c_rate*n;
    
    while(k>0)
    {
        rn1=rand()%n;
        rn2=rand()%n;
        
        if(ppl[rn1]>ppl[rn2])
        {
           c = (ppl[rn1]-ppl[rn2])/4; 
           ppl[rn1]-=c;
           ppl[rn2]+=c;
        }
        else
        {
           c = (ppl[rn2]-ppl[rn1])/4;  
           ppl[rn1]+=c;
           ppl[rn2]-=c;
        }
        
        k--;
    }
    
    
    return;
}

void mutation(float* ppl,int n,float x_l,float x_u,float delta,float m_rate)
{
    int m=m_rate*n,i;
    
    for(i=0;i<m;i++)
    {
        int rn=rand()%n;
        ppl[rn]+=(float)(rand()%2-1)*delta;
    }
    
    return;
}

void selection(float* ppl,int n,float x_l,float x_u,float delta,float s_prop)
{
    float t2;
    int m = s_prop*n,t,i,rn1,rn2;
    float* fitness =(float* )malloc(n*sizeof(float));
    for(i=0;i<n;i++)
    {
        t2=f(ppl[i]);
        fitness[i]=t2*t2;
    }
    
    // we can use any sorting method
    mergesort(ppl,fitness,0,n-1);
    //sort(ppl,fitness,0,n-1);
    
    t=m;
    while(t<n&&m>1)
    {
        rn1=rand()%m;
        rn2=rand()%m;
        ppl[t]=(ppl[rn1]+ppl[rn2])/2;
        t++;
    }
    
    
}

void init_ppl(float* ppl,int n,float x_l,float x_u,float delta)
{
    float temp;
    temp=(x_u-x_l)/delta;
    int rn, m = temp,i;
    
    for(i=0;i<n;i++)
    {
        rn=rand()%m;
        ppl[i]=x_l+delta*(float)rn;
    }
    
    return;
}


int main()
{
    // Hyper parameters of GA
    int generations=10,ppl_size=20,t=0,i;
    float x_l=0,x_u=10,delta=0.01,m_rate=0.1,c_rate=0.95,s_prop=0.5;
    
    float* best_x = (float*)malloc(generations*sizeof(float));
    float* ppl = (float*)malloc(ppl_size*sizeof(float));
    
    init_ppl(ppl,ppl_size,x_l,x_u,delta);
    selection(ppl,ppl_size,x_l,x_u,delta,s_prop);
    
    cout<<"Generation"<< t << " : ";
    for(i=0;i<ppl_size;i++)
    {
        cout<<"("<<ppl[i]<<","<<fit(ppl[i])<<") ";
    }
    cout<<endl;

    t=0;
    while(t<generations)
    {
        crossover(ppl,ppl_size,x_l,x_u,delta,c_rate);
        mutation(ppl,ppl_size,x_l,x_u,delta,m_rate/(1+(float)0*t));
        selection(ppl,ppl_size,x_l,x_u,delta,s_prop);
        
        cout<<"Generation"<< t+1 << " : ";
        for(i=0;i<ppl_size;i++)
        {
            cout<<"("<<ppl[i]<<","<<fit(ppl[i])<<") ";
        }
        cout<<endl;
        
        t++;
    }
    
	return 0;
}
