# Sex vs Asex : Gains in diagonality due to recombination
An Overview:

The question of why sexual replication exists becomes really interesting as you think about it. It seems, at first, to have serious diadvantages when compared to asexual replication strategies. An obvious one being that sexual populations will grow much slower - since they must expend energy and time in finding a mate. If we assume that each organism only has enough energy to contribute to only two offspring, the asexual population can grow exponetially faster than the sexual population.
<p align="center">
  <img width="250" height="140" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Evolsex-dia1a.png/250px-Evolsex-dia1a.png">
</p>

But given the prevalence of sexual replication in nature, there must be some great benefit of replicating in this way. Also, given that even some quite simple organisms replicate sexually (e.g. Bacterial Conjugation), we want out explanation to be as "simple" as possible, avoiding things like selective mating etc.

I'm approaching the question from a mathematical lens. The first stage of my research involved creating a series of simulations, for which this is the code. In these I create two populations, one which replicates sexually and the other which replicates asexually. Each organism's genes are represented by a list of N numbers (e.g. [3132, 6, 1232, 12...]) - we can think about each organisms gene as representing a point in an N-dimensional space (the N here is pre-set). Then we map each sequence of genes to some fitness level. This is easily visualised for the case where N = 2. Here the organisms have a gene sequence of two numbers, say [10, 25] which can be thought of as a point in a 2d plane. Then, to each point in this 2d plane, we assign some fitness value, so you end up getting a hilly landscape like this (gene sequence [10,25] -> loci_0 = 10, loci_1 = 25):
<p align="center">
  <img width="500" height="360" src="images/ele_70_rand_land.png">
</p>

Now in the simulations, I get two populations, the sexual replicators and teh asexuals. Before we have a replication stage however, I have a survival stage. Here, each organism has a chance of dying, depending on the fitness value of thier gene sequence. The higher your fitness value, the more likely you are to survive. I also have mutation stage, where each gene in each organisms sequence has a random chance of mutatating (in the simulations this change normally distributed around 0). This essentially just spreads the population out a little.

After these survival and mutation stages (both blind to whether the populations are sexual or asexual) we have the replication stage. In my simulations, this stage is entirely independent of an organisms fitnesss values - that only matters for survivel. For the asexuals, replication is simply replicating everyone once, and then randomly replicating some organisms to replenish the original stock. 
    
Now in the simulations, I get two populations, one which replicates sexually and the other asexually - this process is entirely independent of the fitness values assigned to each organism. For the asexuals, they simply duplicate themselves. However the sexual replication process is a lot more interesting. In my model, I essentially have the population undergo a super recombination of the genes. It is as if, for each loci (position in the gene sequence) I take the genes (numbers) of the entire population and shuffle them around randomly. So, say I had a sexual population of size 3:  [13, 123], [231, 65], [1123, 14], the first step of the super recombination would suffle the first numbers of each of these organisms randomly, so you might get [231, 123], [13, 65], [1123, 14]. Then we would shuffle the secound numbers in the gene sequence and so on. This shuffling is mathematically equivalent to the population undergoing standard, pair based, sexual mixing lots and lots. Below is a picture illustrating how such sexual recombination effects out population's distribution (in the N=2 case):
<p align="center">
  <img width="900" height="450" src="images/recombination.png">
</p>

As you can see, the population's distribution in each individual loci has remained the same, but the shape of the population has become more 'rectangular'. This is since now each loci's distribution is independent of the other. This 'becoming more rectangular' is the key to why the sexual population is going to be able to move faster in the diagonal direction in fitness landscapes.

The initial results of the simulations have suggested a hypothesis that extends the work of Andrew Lewis Pye's Paper:
Sex vs Asex: the role of varience conversion (https://lewispye.files.wordpress.com/2018/08/svsastp3.pdf). It seems that
the papers results may be generalisable to many different fitness landscapes. Namely, sexual recombination increases varience of the sexual population in 'diagonal' directions, enabling it to move faster into such directions. This enables the sexual population to excel when moving in these 'diagonal' directions confers a fitness advantage. Not only that, but the sexual recombination process entails no disadvantage when moving 'not diagonally', meaning it is competitive in that case also!

(this isn't finished)
