<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Bot;
use App\Repository\BotRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpClient\HttpClient;
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

    /**
     * @Route("/bot/update/{id}")
     */
    public function updateTags(Bot $bot)
    {
        $client = HttpClient::create();
        $response = $client->request('GET', sprintf('http://%s/tags', $bot->getIpAddress()));

        if(200 !== $response->getStatusCode()){
            throw new \RuntimeException('could not fetch tags from bot');
        }

        $info = json_decode($response->getContent(), true);

        $bot->setLeftTag($info['left_tag'] ?? null);
        $bot->setRightTag($info['right_tag'] ?? null);

        $this->botRepository->save($bot);

        return $this->redirectToRoute('app_bot_overview');
    }

    /** @Route("/bot/overview", methods={"GET"}) */
    public function overview(): Response
    {
        return $this->render('bot/overview.html.twig', ['bots' => $this->botRepository->findAll()]);
    }
}
