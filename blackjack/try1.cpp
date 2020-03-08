#include <iostream>
using namespace std;

int* make_permuataion(int n)
{
	int* perm = (int* )malloc(n*sizeof(int));
	int* temp = (int* )malloc(n*sizeof(int));
	int i;
	for(i=0;i<n;i++)temp[i]=i;

	int len=n,rn,idx=0,tt;

	while(len>1)
	{
		rn=rand()%len;
		perm[idx]=temp[rn];

		// swapping len and rn 
		tt=temp[rn];
		temp[rn]=temp[len-1];
		temp[len-1]=tt;

		idx++;
		len--;

	}
	perm[idx]=temp[len-1];


	return perm;
}

void slection(int* scores,int * ppl,int n)
{
	int i;
	// crewate copy of scores
	int* perm = make_permuataion(n);

	// making the tournament between i and perm[i] (compitator of i) and selecting on the basis by just changing the ppl[i] by the ppl[perm[i]], i.e. just chaning the magic number
	for (i=0;i<n;i++)
	{
		if(scores[i]<scores[perm[i]])ppl[i]=ppl[perm[i]];
		
		// accounting for the same score then choose with 50% chance anyone
		if(scores[i]==scores[perm[i]])
		{
			p=rand()%2;
			if(p==0)ppl[i]=ppl[perm[i]];
		}
	}
	
}


void mutate(int * ppl,int n,int m_times,int m_size)
{
	int p,i;
	while(m_times--)
	{
		p=rand()%2;
		i=rand()%n;
		if(p==0)
		{
			if(ppl[i]-m_size>0)ppl[i]-=m_size;
		}
		else
		{
			if(ppl[i]+m_size<22)ppl[i]+=m_size;//bj_limit is assumed to be 21
		}
	}
		
}


void crossover(int * ppl,int n,int c)
{
	int c_size,i,j;

	while(c--)
	{
		// need to update this to not selecet the selceted one again
		i=rand()%n;
		j=rand()%n;
		if(ppl[i]>ppl[j])
		{
			c_size=(ppl[i]-ppl[j])/4;
			ppl[i]-=c_size;
			ppl[j]+=c_size;
		}
		else
		{
			c_size=(ppl[j]-ppl[i])/4;
			ppl[j]-=c_size;
			ppl[i]+=c_size;
		}
	}
	
}

int* runBJ(int* ppl,int n,int bj_limit,int epoch)
{
	int* payoff_of_card = (int* )malloc(14*sizeof(int));
	int size=1000,sumofgambler,sumofdealer,i;
	int* scores = (int* )malloc(n*sizeof(int));
	int* cards = (int* )malloc(14*sizeof(int));
	int temp;

	for(i=0;i<n;i++){scores[i]=0;}
	//init payoff of each card only accounted for after 10 all have eleven value and aces have 1 value
	for(i=0;i<14;i++)
	{
		if(i<10)payoff_of_card[i]=i+1;
		else payoff_of_card[i]=11;
	}

	for(int i = 0; i<=n; i++)
    	{
		while(epoch--)
		{
			sumofgambler = 0;
			sumofdealer = 0;
			
			// drawing the cards out of deck
			for(k=0;k<14;k++){cards[k]=4;} // re_init cards
			while(sumofgambler < ppl[i])
			{

				while(true)
				{
				    temp = rand()%13;
				    while(cards[temp] == 0)
					temp = rand()%13;
				    cards[temp]--;
				    break;
				}
				sumofgambler += payoff_of_card[temp];
			}

			for(int k=0;k<14;k++){cards[k]=4;} 


			    if(sumofgambler > bj_limit)
			    {
				scores[i] -=1;
				continue;
			    }
			    while(sumofdealer < bj_limit && sumofdealer < sumofgambler)
			    {
				while(true)
				{
				    temp = rand()%13;
				    while(cards[temp] == 0)
					temp = rand()%13;
				    cards[temp]--;
				    break;
				}
				sumofdealer += payoff_of_card[temp];
			    }
			    if(sumofdealer > bj_limit)
				scores[i] +=1;
			    else if(sumofdealer > sumofgambler)
				scores[i] -=1;
			}
	    }


	return scores;
}



int main()
{
	int ppl_size=100,bj_limit=21,times=100,epoch=1000,i,t=0;

	int* ppl=(int* )malloc(ppl_size*sizeof(int));
	int* scores=(int* )malloc(ppl_size*sizeof(int));
	float* avg_ppl = (float* )malloc(t*sizeof(float));
	float* avg_score = (float* )malloc(t*sizeof(float));
	for(i=0;i<ppl_size;i++)
	{
		ppl[i]=rand()%bj_limit+1;
	}
	scores=runBJ(ppl,ppl_size,bj_limit,epoch);
	
	int sum=0,s_sum=0;
	for(i=0;i<ppl_size;i++)
	{
	    sum+=ppl[i];
	    s_sum+=scores[i];
	}
	
	avg_ppl[t]=(float)sum/ppl_size;
	avg_score[t]=(float)s_sum/ppl_size;
	t++;

	while(t<times)
	{

		slection(scores,ppl,ppl_size);

		crossover(ppl,ppl_size,15); // 15 crossovers note not accounted for stopping crossover of one many times

		mutate(ppl,ppl_size,6,1); // 6 times with 1 as mutation size // note there is no limit on capping mutated  value by 21 , add it as if one had 20 and then mutated by 2 gives 22

		scores=runBJ(ppl,ppl_size,bj_limit,epoch);
		
		int sum=0,s_sum=0;
		for(i=0;i<ppl_size;i++)
		{
		    sum+=ppl[i];
		    s_sum+=scores[i];
		}
		
		avg_ppl[t]=(float)sum/ppl_size;
		avg_score[t]=(float)s_sum/ppl_size;
		t++;
	}

	for(i=0;i<t;i++)
	{
		cout<<" Average solution at "<<i+1<<"'th "<<"is "<<avg_ppl[i]<< " with avg score as " << avg_score[i] <<endl;
	}
	
	return 0;
}
