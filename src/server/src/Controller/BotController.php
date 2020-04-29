<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Bot;
use App\Repository\BotRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class BotController extends AbstractController
{
    private $botRepository;

    public function __construct(BotRepository $botRepository)
    {
        $this->botRepository = $botRepository;
    }

    /** @Route("/bot/register", methods={"GET"}) */
    public function register(Request $request): Response
    {
        $ip = $request->getClientIp();

        $bot = $this->botRepository->findOneByIpAddress($ip);
        if ($bot) {
            // already registered

            return new Response('already registered');
        }

        $bot = new Bot($ip);
        $this->botRepository->save($bot);
        return new Response('successfully registered');
    }

    /** @Route("/bot/overview", methods={"GET"}) */
    public function overview(): Response
    {
        return $this->render('bot/overview.html.twig', ['bots' => $this->botRepository->findAll()]);
    }
}
