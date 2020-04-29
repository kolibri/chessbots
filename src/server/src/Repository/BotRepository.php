<?php

namespace App\Repository;

use App\Entity\Bot;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method Bot|null find($id, $lockMode = null, $lockVersion = null)
 * @method Bot|null findOneBy(array $criteria, array $orderBy = null)
 * @method Bot[]    findAll()
 * @method Bot[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class BotRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Bot::class);
    }

    public function findOneByIpAddress(string $value): ?Bot
    {
        return $this->createQueryBuilder('b')
            ->andWhere('b.ipAddress = :val')
            ->setParameter('val', $value)
            ->getQuery()
            ->getOneOrNullResult()
        ;
    }

    public function save(Bot $bot, bool $flush = true): void
    {
        $entityManager = $this->getEntityManager();
        $entityManager->persist($bot);
        $flush && $entityManager->flush();
    }
}
