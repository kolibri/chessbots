<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\BotRepository")
 */
class Bot
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $ipAddress;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $leftTag;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $rightTag;

    public function __construct(string $ipAddress)
    {
        $this->ipAddress = $ipAddress;
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getIpAddress(): ?string
    {
        return $this->ipAddress;
    }

    public function getLeftTag()
    {
        return $this->leftTag;
    }

    public function setLeftTag($leftTag)
    {
        $this->leftTag = $leftTag;
    }

    public function getRightTag()
    {
        return $this->rightTag;
    }

    public function setRightTag($rightTag)
    {
        $this->rightTag = $rightTag;
    }
}
